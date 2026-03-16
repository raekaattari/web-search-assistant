# create customer service chatbot wth client-side tools 
# look up customer info, get order details, cancel orders 


import anthropic 
import json

client = anthropic.Client()
MODEL_NAME="claude-opus-4-1"

# defining the tools the model can use 
tools = [
    {
        "name": "get_customer_info",
        "description": "gets customer info based on their id",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "unique Id"
                }
            },
            "required": ["customer_id"]
        },
    },
    {
        "name": "get_order_details",
        "description": "Gets the details of a specific order based on order id",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "unique id for the order",
                }
            
            },
            "required": ["order_id"],
        },
       
    },
    {
        "name": "cancel_order",
        "description": "cancels order based on the order_id", 
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "unique id for the order",
                }
            },
            "required": ["order_id"],
        },
    },
]

# mock data 

def get_customer_info(customer_id):
    customers={
        "C1": {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"},
        "C2": {"name": "Jane Smith", "email": "jane@example.com", "phone": "987-654-3210"},
    }
    return customers.get(customer_id, "Customer not found")

def get_order_details(order_id): 
    orders = {
        "O1": {
            "id": "O1",
            "product": "Widget A",
            "quantity": 2,
            "price": 19.99,
            "status": "Shipped",
        },
        "O2": {
            "id": "O2",
            "product": "Gadget B",
            "quantity": 1,
            "price": 49.99,
            "status": "Processing",
        },
    }
    return orders.get(order_id, "Order not found")

def cancel_order(order_id):
    if order_id in ["O1", "O2"]:
        return True
    else:
        return False
    

def process_tool_call(tool_name, tool_input):
    if tool_name == "get_customer_info":
        return get_customer_info(tool_input["customer_id"])
    elif tool_name == "get_order_details":
        return get_order_details(tool_input["order_id"])
    elif tool_name == "cancel_order":
        return cancel_order(tool_input["order_id"])    


def chatbot_interaction(user_message):
    print(f"User Message: {user_message}")
    
    messages = [{"role": "user", "content": user_message}]

    response=client.messages.create(
        model=MODEL_NAME, max_tokens=4096, tools=tools, messages=messages
    )

    print(f"Initial response: stop reason {response.stop_reason}")
    print(f"Initial response: content {response.content}")

    while response.stop_reason == "tool_use":
        tool_uses = []
        for block in response.content: 
            if block.type == "tool_use":
                tool_uses.append(block)


        tool_results =[]
        for tool_use in tool_uses: 
            tool_name = tool_use.name
            tool_input = tool_use.input

            print(f"Tool used: {tool_name}")
            print(f"Tool input: {json.dumps(tool_input, indent=2)}")

            tool_result = process_tool_call(tool_name, tool_input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": str(tool_result)
            })
            print("Tool Result")
            print(json.dumps(tool_result, indent=2))


        messages = [ 
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": tool_results
            },
        ]

        response = client.messages.create(
            model=MODEL_NAME, max_tokens=4096, tools=tools, messages=messages
        )

        print("Response 2:")
        print(f"Stop Reason: {response.stop_reason}")
        print(f"Content: {response.content}")

        final_response = next(
        (block.text for block in response.content if hasattr(block, "text")),
        None,
    )
        
    print(f"Final Response: {final_response}")
    return final_response



print(chatbot_interaction("Can you look up customer C1 and tell me if their email matches order O1?"))