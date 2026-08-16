from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/compile")
async def compile_project(request: Request):
    data = await request.json()
    
    # Generate basic React Native boilerplate
    compiled_code = "import React from 'react';\nimport { View, Text, Button, TextInput, Image, StyleSheet } from 'react-native';\n\nexport default function App() {\n  return (\n    <View style={styles.container}>\n"
    
    # Loop through the JSON components and map them to React Native components
    for component in data:
        if component['type'] == 'Button':
            compiled_code += f"      <Button title='{component['properties']['text']}' onPress={{() => {{}}}} />\n"
        elif component['type'] == 'Text Input':
            compiled_code += f"      <TextInput placeholder='{component['properties']['text']}' style={{borderWidth: 1}} />\n"
        elif component['type'] == 'Image':
            compiled_code += "      <Image source={{uri: 'https://via.placeholder.com/150'}} style={{width: 50, height: 50}} />\n"
    
    compiled_code += "    </View>\n  );\n}\n\nconst styles = StyleSheet.create({\n  container: {\n    flex: 1,\n    justifyContent: 'center',\n    alignItems: 'center',\n  }\n});"
    
    return {"status": "success", "compiled_code": compiled_code}

