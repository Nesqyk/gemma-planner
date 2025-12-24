import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re

import voice_engine
import calendar_tool

print("Loading FunctionGemma... (runs locally)")
model_id = "google/functiongemma-270m-it"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="cpu", 
    torch_dtype=torch.float32
)

tools = [
    {
        "name": "schedule_event",
        "description": "Schedules a calendar event or meeting.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Title of the event"},
                "start_time": {"type": "string", "description": "ISO 8601 start time (YYYY-MM-DDTHH:MM:SS)"},
                "duration_minutes": {"type": "integer", "description": "Duration in minutes"}
            },
            "required": ["summary", "start_time"]
        }
    }
]

def parse_function_call(response_text):
    pattern = r"call:(\w+)\{(.*?)\}"
    match = re.search(pattern, response_text)
    
    if match:
        func_name = match.group(1)
        args_str = match.group(2)
        
        args = {}
        parts = args_str.split(',') 
        for part in parts:
            if ':' in part:
                key, val = part.split(':', 1)
                val = val.replace('"', '').replace("'", "").strip()
                args[key.strip()] = val
        return func_name, args
    return None, None

def run_agent():
    voice_engine.speak("System online. What is your plan?")
    
    while True:

        user_text = voice_engine.listen()
        
        if not user_text:
            continue
            
        if "exit" in user_text.lower() or "quit" in user_text.lower():
            voice_engine.speak("Shutting down.")
            break

        messages = [
            {"role": "developer", "content": "You are a helpful assistant. You can call functions. Default to today's date (2025-12-24) if not specified."},
            {"role": "user", "content": user_text}
        ]
        
        inputs = tokenizer.apply_chat_template(
            messages,
            tools=tools,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True
        )

        outputs = model.generate(**inputs, max_new_tokens=128)
        response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=False)
        
        if "<start_function_call>" in response:
            func_name, args = parse_function_call(response)
            
            if func_name == "schedule_event":
                voice_engine.speak(f"Scheduling {args.get('summary')}...")
                
                success = calendar_tool.create_ics_event(
                    args.get('summary'),
                    args.get('start_time'),
                    int(args.get('duration_minutes', 60))
                )
                
                if success:
                    voice_engine.speak("Done. Please check the popup.")
        else:
            clean_response = response.replace("<end_of_turn>", "").strip()
            voice_engine.speak(clean_response)

if __name__ == "__main__":
    run_agent()