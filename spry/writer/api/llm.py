"""LLM API integration for content generation"""

import frappe
import sys
import json
import requests
import importlib.util
from urllib.parse import urljoin

# Try to import provider-specific libraries
def check_dependency(module_name):
    """Check if a Python module is installed and can be imported"""
    return importlib.util.find_spec(module_name) is not None

# Check for provider dependencies
HAS_OPENAI = check_dependency("openai")
HAS_ANTHROPIC = check_dependency("anthropic")
HAS_GOOGLE_GENAI = check_dependency("google.generativeai")

# Import libraries if available
if HAS_OPENAI:
    import openai
if HAS_ANTHROPIC:
    import anthropic
if HAS_GOOGLE_GENAI:
    import google.generativeai as genai


@frappe.whitelist()
def call_llm(prompt: str, provider: str, model: str) -> str:
    """
    Main dispatch function for calling different LLM providers.
    
    Args:
        prompt (str): The input prompt to send to the LLM
        provider (str): The LLM provider name (OpenAI, Anthropic, Google, etc.)
        model (str): The specific model to use within the provider
        
    Returns:
        str: The generated text response from the LLM
        
    Raises:
        frappe.ValidationError: If the API key is not set or provider is not supported
    """
    provider = provider.lower()
    
    # Get the API key for the selected provider
    api_key_dict = get_llm_api_key(provider)
    api_key = api_key_dict.get("api_key")
    
    if not api_key:
        frappe.throw(f"API key for '{provider}' is not set. Please configure it in your LLM Settings.")
    
    # Use dynamic function dispatch pattern to call the appropriate provider handler
    normalized_provider = provider.lower().replace('-', '_').replace(' ', '_')
    handler_name = f"_call_{normalized_provider}_llm"
    
    current_module = sys.modules[__name__]
    
    if hasattr(current_module, handler_name):
        handler_func = getattr(current_module, handler_name)
        return handler_func(prompt, model, api_key)
    else:
        frappe.log_error(f"No handler found for provider '{provider}'", "LLM Provider Error")
        frappe.throw(f"Provider '{provider}' is not supported yet.")


def _call_openai_llm(prompt: str, model: str, api_key: str) -> str:
    """Call OpenAI's API to generate content."""
    if not HAS_OPENAI:
        frappe.throw("The OpenAI package is not installed. Please run 'pip install openai' to install it.")
        
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates high-quality content."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "OpenAI API Call Failed")
        frappe.throw(f"An error occurred while calling the OpenAI API: {str(e)}")


def _call_anthropic_llm(prompt: str, model: str, api_key: str) -> str:
    """Call Anthropic's API to generate content."""
    if not HAS_ANTHROPIC:
        frappe.throw("The Anthropic package is not installed. Please run 'pip install anthropic' to install it.")
        
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Anthropic API Call Failed")
        frappe.throw(f"An error occurred while calling the Anthropic API: {str(e)}")


def _call_google_llm(prompt: str, model: str, api_key: str) -> str:
    """Call Google's Gemini API to generate content."""
    if not HAS_GOOGLE_GENAI:
        frappe.throw("The Google GenAI package is not installed. Please run 'pip install google-generativeai' to install it.")
        
    try:
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        return response.text
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Google API Call Failed")
        frappe.throw(f"An error occurred while calling the Google API: {str(e)}")


def _call_groq_llm(prompt: str, model: str, api_key: str) -> str:
    """Call Groq's API to generate content using OpenAI's compatible interface."""
    if not HAS_OPENAI:
        frappe.throw("The OpenAI package is not installed. Please run 'pip install openai' to install it.")
    
    try:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates high-quality content."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Groq API Call Failed")
        frappe.throw(f"An error occurred while calling the Groq API: {str(e)}")


def _call_ollama_llm(prompt: str, model: str, api_key: str) -> str:
    """Call Ollama's API to generate content."""
    try:
        base_url = api_key.strip()
        if not base_url.endswith("/"):
            base_url = base_url + "/"
            
        endpoint = urljoin(base_url, "api/chat")
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that generates high-quality content."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        
        return result.get("message", {}).get("content", "")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Ollama API Call Failed")
        frappe.throw(f"An error occurred while calling the Ollama API: {str(e)}")


@frappe.whitelist()
def set_llm_api_key(provider: str, api_key: str):
    """Set LLM API key for a provider"""
    user = frappe.session.user
    llm_settings_name = frappe.db.exists("LLM Settings", {"user": user})

    if llm_settings_name:
        doc = frappe.get_doc("LLM Settings", llm_settings_name)
    else:
        doc = frappe.new_doc("LLM Settings")
        doc.user = user

    # Check if the provider already exists
    provider_exists = False
    for setting in doc.provider_settings:
        if setting.provider == provider:
            setting.api_key = api_key
            provider_exists = True
            break

    if not provider_exists:
        doc.append("provider_settings", {
            "provider": provider,
            "api_key": api_key
        })

    doc.save(ignore_permissions=True)
    return {"status": "success"}


@frappe.whitelist()
def get_llm_api_key(provider: str):
    """Get LLM API key for the specified provider"""
    provider_normalized = provider.lower()
    
    # Try to get user-specific API key
    user = frappe.session.user
    llm_settings_name = frappe.db.exists("LLM Settings", {"user": user})

    if llm_settings_name:
        doc = frappe.get_doc("LLM Settings", llm_settings_name)
        for setting in doc.provider_settings:
            if setting.provider.lower() == provider_normalized:
                api_key = setting.get_password("api_key")
                if api_key:
                    return {"api_key": api_key}

    # No API key found
    return {}


@frappe.whitelist()
def get_llm_providers():
    """Get list of supported LLM providers"""
    return [
        {"name": "OpenAI", "value": "openai"},
        {"name": "Anthropic", "value": "anthropic"},
        {"name": "Google", "value": "google"},
        {"name": "Groq", "value": "groq"},
        {"name": "Ollama", "value": "ollama"}
    ]


@frappe.whitelist()
def get_llm_models(provider: str):
    """Get list of available models for a provider"""
    provider = provider.lower()
    
    models = {
        "openai": [
            {"name": "gpt-4o", "value": "gpt-4o"},
            {"name": "gpt-4o-mini", "value": "gpt-4o-mini"},
            {"name": "gpt-4-turbo", "value": "gpt-4-turbo"},
            {"name": "gpt-3.5-turbo", "value": "gpt-3.5-turbo"}
        ],
        "anthropic": [
            {"name": "Claude 3.5 Sonnet", "value": "claude-3-5-sonnet-20241022"},
            {"name": "Claude 3 Opus", "value": "claude-3-opus-20240229"},
            {"name": "Claude 3 Sonnet", "value": "claude-3-sonnet-20240229"},
            {"name": "Claude 3 Haiku", "value": "claude-3-haiku-20240307"}
        ],
        "google": [
            {"name": "Gemini 1.5 Pro", "value": "gemini-1.5-pro"},
            {"name": "Gemini 1.5 Flash", "value": "gemini-1.5-flash"},
            {"name": "Gemini Pro", "value": "gemini-pro"}
        ],
        "groq": [
            {"name": "Llama 3.1 70B", "value": "llama-3.1-70b-versatile"},
            {"name": "Llama 3.1 8B", "value": "llama-3.1-8b-instant"},
            {"name": "Mixtral 8x7B", "value": "mixtral-8x7b-32768"}
        ],
        "ollama": [
            {"name": "Llama 3.2", "value": "llama3.2"},
            {"name": "Llama 3.1", "value": "llama3.1"},
            {"name": "Mistral", "value": "mistral"},
            {"name": "Phi 3", "value": "phi3"}
        ]
    }
    
    return models.get(provider, [])
