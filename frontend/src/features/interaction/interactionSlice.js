import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  draft: {},
  chatHistory: [],
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    setDraft: (state, action) => {
      state.draft = action.payload;
    },
    addMessage: (state, action) => {
      state.chatHistory.push(action.payload);
    },
  },
});

export const { setDraft, addMessage } = interactionSlice.actions;
export default interactionSlice.reducer;