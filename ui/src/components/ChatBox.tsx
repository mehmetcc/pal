"use client";

import React, { useState } from "react";

type Message = {
    id: number;
    sender: "user" | "bot";
    text: string;
    created_at: string;
};

const ChatBox: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage: Message = {
            id: messages.length + 1,
            sender: "user",
            text: input,
            created_at: new Date().toISOString(),
        };

        setMessages([...messages, userMessage]);

        try {
            const response = await fetch("/api/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input }),
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();

            const botMessage: Message = {
                id: messages.length + 2,
                sender: "bot",
                text: data.response || "No response",
                created_at: data.created_at || new Date().toISOString(),
            };

            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            console.error(error);
            setMessages((prev) => [
                ...prev,
                {
                    id: messages.length + 2,
                    sender: "bot",
                    text: "Error fetching response",
                    created_at: new Date().toISOString(),
                },
            ]);
        }

        setInput("");
    };

    return (
        <div className="flex flex-col w-full h-full p-4 bg-gray-100">
            <div className="flex-grow overflow-y-auto bg-white shadow rounded-lg p-4">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`p-2 rounded-lg my-2 ${message.sender === "user"
                                ? "bg-blue-500 text-white self-end"
                                : "bg-gray-300 text-black self-start"
                            }`}
                    >
                        <p>{message.text}</p>
                        <small className="text-xs text-gray-500">
                            {new Date(message.created_at).toLocaleString()}
                        </small>
                    </div>
                ))}
            </div>
            <div className="flex mt-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-grow p-2 border border-gray-300 rounded-l-lg"
                    placeholder="Type a message..."
                />
                <button
                    onClick={handleSend}
                    className="px-4 bg-blue-500 text-white rounded-r-lg"
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default ChatBox;
