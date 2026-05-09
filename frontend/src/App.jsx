import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";

import { addMessage, setDraft } from "./features/interaction/interactionSlice";

function App() {
  const [message, setMessage] = useState("");
  const [saveStatus, setSaveStatus] = useState("");

  const dispatch = useDispatch();
  const draft = useSelector((state) => state.interaction.draft);
  const chatHistory = useSelector((state) => state.interaction.chatHistory);

  const sendMessage = async () => {
    if (!message.trim()) return;

    dispatch(addMessage({ role: "user", content: message }));

    try {
      const response = await axios.post("http://127.0.0.1:8000/agent/chat", {
        message,
        current_draft: draft,
      });

      dispatch(
        addMessage({
          role: "assistant",
          content: response.data.assistant_response,
        })
      );

      dispatch(setDraft(response.data.updated_draft));
      setMessage("");
    } catch (error) {
      console.error(error);
    }
  };

  const saveInteraction = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/interaction/save",
        draft
      );

      setSaveStatus(`Saved successfully. Interaction ID: ${response.data.interaction_id}`);
    } catch (error) {
      console.error(error);
      setSaveStatus("Failed to save interaction.");
    }
  };

  return (
    <div style={pageStyle}>
      <div style={leftPanelStyle}>
        <div style={topBarStyle}>
          <div>
            <h1 style={titleStyle}>Log HCP Interaction</h1>
            <p style={subtitleStyle}>
              Capture field activity through structured data and AI assistance.
            </p>
          </div>
          <div style={statusPillStyle}>Draft</div>
        </div>

        <SectionTitle title="Interaction Details" />

        <div style={gridStyle}>
          <InputField label="HCP Name" value={draft.hcp_name} />
          <InputField label="Interaction Type" value={draft.interaction_type} />
        </div>

        <div style={gridStyle}>
          <InputField label="Products Discussed" value={draft.products_discussed} />
          <InputField label="Samples Distributed" value={draft.samples_distributed} />
        </div>

        <InputField label="Materials Shared" value={draft.materials_shared} />
        <SentimentField value={draft.sentiment} />
        <TextAreaField label="Summary" value={draft.summary} />
        <TextAreaField label="Follow Up Action" value={draft.follow_up_action} />

        {draft.next_best_action && (
          <TextAreaField label="Next Best Action" value={draft.next_best_action} />
        )}

        {draft.hcp_profile && (
          <TextAreaField
            label="HCP Profile"
            value={`Specialty: ${draft.hcp_profile.specialty}\nPreferred Channel: ${draft.hcp_profile.preferred_channel}\nLast Interaction: ${draft.hcp_profile.last_interaction}`}
          />
        )}

        <ComplianceBadge value={draft.compliance_risk} />

        <div style={saveAreaStyle}>
          <button onClick={saveInteraction} style={saveButtonStyle}>
            Save Interaction
          </button>

          {saveStatus && <div style={saveStatusStyle}>{saveStatus}</div>}
        </div>
      </div>

      <div style={rightPanelStyle}>
        <div style={assistantHeaderStyle}>
          <div style={assistantTitleStyle}>AI Assistant</div>
          <div style={assistantSubtitleStyle}>
            Use natural language to populate or update the form.
          </div>
        </div>

        <div style={chatAreaStyle}>
          {chatHistory.length === 0 && (
            <div style={emptyStateStyle}>
              Try: “Met Dr. Sharma today and discussed CardioX. Shared brochure
              and 2 samples.”
            </div>
          )}

          {chatHistory.map((chat, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                justifyContent: chat.role === "user" ? "flex-end" : "flex-start",
                marginBottom: "10px",
              }}
            >
              <div
                style={{
                  maxWidth: "88%",
                  padding: "10px 12px",
                  borderRadius: "10px",
                  lineHeight: "1.45",
                  fontSize: "13px",
                  background: chat.role === "user" ? "#2563eb" : "#f1f5f9",
                  color: chat.role === "user" ? "white" : "#111827",
                  border: chat.role === "assistant" ? "1px solid #e2e8f0" : "none",
                }}
              >
                {chat.content}
              </div>
            </div>
          ))}
        </div>

        <div style={inputBarStyle}>
          <textarea
            rows={1}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe interaction..."
            style={textareaStyle}
          />

          <button onClick={sendMessage} style={buttonStyle}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const pageStyle = {
  display: "flex",
  height: "100vh",
  background: "#f8fafc",
  padding: "14px",
  gap: "12px",
  fontFamily: "Inter, Arial, sans-serif",
  boxSizing: "border-box",
};

const leftPanelStyle = {
  width: "72%",
  background: "white",
  borderRadius: "10px",
  padding: "20px",
  overflowY: "auto",
  boxShadow: "0 1px 6px rgba(15, 23, 42, 0.08)",
};

const rightPanelStyle = {
  width: "28%",
  background: "white",
  borderRadius: "10px",
  display: "flex",
  flexDirection: "column",
  boxShadow: "0 1px 6px rgba(15, 23, 42, 0.08)",
};

const topBarStyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "flex-start",
  marginBottom: "20px",
};

const titleStyle = {
  fontSize: "26px",
  margin: 0,
  color: "#111827",
  fontWeight: "700",
};

const subtitleStyle = {
  margin: "6px 0 0",
  color: "#64748b",
  fontSize: "13px",
};

const statusPillStyle = {
  padding: "6px 12px",
  borderRadius: "999px",
  background: "#eff6ff",
  color: "#2563eb",
  fontSize: "12px",
  fontWeight: "600",
};

const gridStyle = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "12px",
  marginBottom: "12px",
};

const assistantHeaderStyle = {
  padding: "16px",
  borderBottom: "1px solid #e5e7eb",
};

const assistantTitleStyle = {
  fontSize: "20px",
  fontWeight: "700",
  color: "#1e40af",
};

const assistantSubtitleStyle = {
  marginTop: "4px",
  color: "#64748b",
  fontSize: "12px",
  lineHeight: "1.4",
};

const chatAreaStyle = {
  flex: 1,
  overflowY: "auto",
  padding: "14px",
};

const emptyStateStyle = {
  padding: "12px",
  borderRadius: "10px",
  background: "#f8fafc",
  border: "1px dashed #cbd5e1",
  color: "#64748b",
  fontSize: "13px",
  lineHeight: "1.5",
};

const inputBarStyle = {
  padding: "12px",
  borderTop: "1px solid #e5e7eb",
  display: "flex",
  gap: "8px",
};

const textareaStyle = {
  flex: 1,
  resize: "none",
  borderRadius: "9px",
  border: "1px solid #d1d5db",
  padding: "10px",
  fontSize: "13px",
  outline: "none",
};

const buttonStyle = {
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "9px",
  padding: "0 16px",
  cursor: "pointer",
  fontWeight: "600",
  fontSize: "13px",
};

const saveAreaStyle = {
  marginTop: "14px",
  display: "flex",
  alignItems: "center",
  gap: "12px",
};

const saveButtonStyle = {
  background: "#16a34a",
  color: "white",
  border: "none",
  borderRadius: "9px",
  padding: "11px 16px",
  cursor: "pointer",
  fontWeight: "600",
  fontSize: "13px",
};

const saveStatusStyle = {
  color: "#166534",
  fontSize: "13px",
  fontWeight: "600",
};

function SectionTitle({ title }) {
  return <div style={sectionTitleStyle}>{title}</div>;
}

const sectionTitleStyle = {
  marginBottom: "12px",
  fontSize: "16px",
  fontWeight: "700",
  color: "#334155",
};

function InputField({ label, value }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <div style={fieldLabelStyle}>{label}</div>
      <div style={inputBoxStyle}>{value || "-"}</div>
    </div>
  );
}

function TextAreaField({ label, value }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <div style={fieldLabelStyle}>{label}</div>
      <div style={textAreaBoxStyle}>{value || "-"}</div>
    </div>
  );
}

const fieldLabelStyle = {
  marginBottom: "6px",
  fontWeight: "600",
  color: "#334155",
  fontSize: "13px",
};

const inputBoxStyle = {
  padding: "10px",
  borderRadius: "8px",
  border: "1px solid #d1d5db",
  background: "#f9fafb",
  minHeight: "20px",
  fontSize: "13px",
  color: "#111827",
};

const textAreaBoxStyle = {
  padding: "10px",
  borderRadius: "8px",
  border: "1px solid #d1d5db",
  background: "#f9fafb",
  minHeight: "60px",
  lineHeight: "1.5",
  whiteSpace: "pre-line",
  fontSize: "13px",
  color: "#111827",
};

function SentimentField({ value }) {
  return (
    <div style={{ marginBottom: "14px" }}>
      <div style={fieldLabelStyle}>Observed/Inferred HCP Sentiment</div>
      <div style={{ display: "flex", gap: "10px" }}>
        <SentimentOption active={value === "positive"} label="Positive" />
        <SentimentOption active={value === "neutral"} label="Neutral" />
        <SentimentOption active={value === "negative"} label="Negative" />
      </div>
    </div>
  );
}

function SentimentOption({ label, active }) {
  return (
    <div
      style={{
        padding: "7px 12px",
        borderRadius: "999px",
        background: active ? "#dbeafe" : "#f8fafc",
        border: active ? "1px solid #2563eb" : "1px solid #e5e7eb",
        color: active ? "#1d4ed8" : "#475569",
        fontWeight: "600",
        fontSize: "12px",
      }}
    >
      {label}
    </div>
  );
}

function ComplianceBadge({ value }) {
  const isHigh = value === "high";

  return (
    <div
      style={{
        marginTop: "14px",
        padding: "11px 12px",
        borderRadius: "9px",
        background: isHigh ? "#fee2e2" : "#dcfce7",
        color: isHigh ? "#991b1b" : "#166534",
        fontWeight: "600",
        fontSize: "13px",
      }}
    >
      Compliance Risk: {value || "low"}
    </div>
  );
}

export default App;