# streamlit_app.py — Screenshot-styled popup chatbot (server-side Gemini)
# ----------------------------------------------------------------------
# pip install streamlit google-generativeai
# PowerShell example:
#   $env:GOOLE_API_KEY="YOUR_KEY_HERE"
# Run:
#   streamlit run streamlit_app.py
# ----------------------------------------------------------------------

from __future__ import annotations
import os, html
import streamlit as st
import google.generativeai as genai

import streamlit as st
from streamlit.components.v1 import html

st.markdown("""
<div class="chatbot-root">
  <!-- Toggle (no JS needed) -->
  <input type="checkbox" id="chatbot-toggle" hidden>

  <!-- Floating icon -->
  <label id="chatbot-icon" for="chatbot-toggle" title="Open chat">💬</label>

  <!-- Popup -->
  <div id="chatbot-container" role="dialog" aria-modal="true" aria-label="ChatBot">
    <div id="chatbot-header">
      <span>ChatBot</span>
      <label id="close-btn" for="chatbot-toggle" aria-label="Close">&times;</label>
    </div>
    <div id="chatbot-body">
      <div id="chatbot-messages">
        <div class="message bot">Hi! How can I help?</div>
      </div>
    </div>
    <div id="chatbot-input-container">
      <input type="text" id="chatbot-input" placeholder="Type a message" />
      <button id="send-btn" type="button">Send</button>
    </div>
  </div>
</div>

<style>
  /* Make sure these float above Streamlit UI */
  #chatbot-icon, #chatbot-container { z-index: 10000; }

  /* Root anchored to viewport, not to Streamlit blocks */
  .chatbot-root {
    position: fixed;
    inset: 0;              /* span viewport so fixed children align correctly */
    pointer-events: none;  /* allow clicks through except on our elements */
  }

  /* Floating Chat Icon */
  #chatbot-icon {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px; height: 60px;
    background: blue; color: #fff; font-size: 30px;
    display: flex; justify-content: center; align-items: center;
    border-radius: 50%;
    box-shadow: 0 0 15px rgba(0,0,0,.4);
    cursor: pointer;
    transition: transform .2s, background-color .2s;
    pointer-events: auto; /* re-enable clicks */
  }
  #chatbot-icon:hover { background: #b71c1c; transform: scale(1.1); }

  /* Popup */
  #chatbot-container {
    position: fixed;
    bottom: 80px; right: 20px;
    width: 350px; height: 450px;
    background: #1f1f1f; border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,0,0,.6);
    display: flex; flex-direction: column; overflow: hidden;

    /* hidden by default */
    opacity: 0; transform: translateY(10px) scale(.98);
    pointer-events: none;
    transition: opacity .18s ease, transform .18s ease;
  }

  /* Toggle on when checked */
  #chatbot-toggle:checked ~ #chatbot-container {
    opacity: 1; transform: translateY(0) scale(1);
    pointer-events: auto;
  }

  /* Header */
  #chatbot-header {
    background: blue; color: #fff; padding: 15px;
    border-top-left-radius: 15px; border-top-right-radius: 15px;
    display: flex; justify-content: space-between; align-items: center; font-size: 18px;
  }
  #close-btn {
    background: none; border: none; color: #fff; font-size: 22px;
    line-height: 1; cursor: pointer; padding: 0; margin: 0;
    pointer-events: auto; /* clickable */
  }

  /* Body + messages */
  #chatbot-body { flex: 1; padding: 10px; overflow-y: auto; }
  #chatbot-messages { display: flex; flex-direction: column; }
  .message { margin-bottom: 15px; padding: 12px; border-radius: 8px; max-width: 85%; }
  .message.user { background: blue; color: #fff; align-self: flex-end; }
  .message.bot  { background: #333; color: #fff; align-self: flex-start; }

  /* Input row */
  #chatbot-input-container { display: flex; padding: 10px; border-top: 1px solid #444; background: #2c2c2c; }
  #chatbot-input {
    flex: 1; padding: 10px; border: 1px solid #444; border-radius: 10px;
    background: #333; color: #fff;
  }
  #send-btn {
    margin-left: 10px; padding: 10px 15px; background: blue; color: #fff;
    border: none; border-radius: 8px; cursor: pointer; font-size: 16px;
  }
  #send-btn:hover { background: #b71c1c; }
</style>
""", unsafe_allow_html=True)
