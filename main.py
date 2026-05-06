import argparse
import json
import os
from enum import auto

import lmstudio as lms
from openai import OpenAI

from prompts import system_prompt
from tools import call_function, tools

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "google/gemma-4-26b-a4b"


parser = argparse.ArgumentParser(description="Localbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [{"role": "system", "content": system_prompt}]

messages.append({"role": "user", "content": args.user_prompt})


def process_tool_calls(response, messages):
    tool_calls = response.choices[0].message.tool_calls

    assistant_tool_call_message = {
        "role": "assistant",
        "tool_calls": [
            {
                "id": tool_call.id,
                "type": tool_call.type,
                "function": tool_call.function,
            }
            for tool_call in tool_calls
        ],
    }

    messages.append(assistant_tool_call_message)

    tool_results = []
    for tool_call in tool_calls:
        tool_call_result = call_function(tool_call, args.verbose)

        tool_results.append(tool_call_result)
        messages.append(tool_call_result)
        if args.verbose:
            print(f"Result ->\n{json.loads(tool_call_result['content'])}")

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return final_response


def main():
    for _ in range(25):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.4,
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content,
                }
            )
            # print("Stage Response: ", response.choices[0].message.reasoning_content)
            # print("Stage Tools: ", response.choices[0].message.tool_calls)
            if response.choices[0].message.tool_calls:
                final_response = process_tool_calls(response, messages)
                # print(
                #    "\nAssistant:",
                #    final_response.choices[0].message.reasoning_content,
                # )

                messages.append(
                    {
                        "role": "assistant",
                        "content": final_response.choices[0].message.reasoning_content,
                    }
                )
            else:
                print(
                    "\nAssistant:",
                    response.choices[0].message.content,
                )

                messages.append(
                    {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
                    }
                )
                break
                # elif response.choices[0].message.reasoning_content:
                # print(
                #    "\nAssistant:",
                #    response.choices[0].message.reasoning_content,
                # )

        except Exception as e:
            print(f"\nAn error occurred: {e}")
            exit(1)


if __name__ == "__main__":
    main()
