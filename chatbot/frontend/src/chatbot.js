// src/Chatbot.js
import React, { useState } from 'react';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = async () => {
        try {
            const response = await fetch('http://localhost:5002/get-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input }),
            });
            
            // Asegúrate de que la respuesta sea correcta
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const data = await response.json();
    
            // Actualiza el estado con el nuevo mensaje y la respuesta del chatbot
            setMessages([...messages, { user: input, bot: data.response }]);
            setInput('');
        } catch (error) {
            console.error('Error fetching response:', error);
        }
    };
    

    return (
        <div>
            <div>
                {messages.map((msg, index) => (
                    <div key={index}>
                        <strong>Tú:</strong> {msg.user}<br />
                        <strong>Chatbot:</strong> {msg.bot}<br />
                    </div>
                ))}
            </div>
            <input 
                type="text" 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <button onClick={handleSend}>Enviar</button>
        </div>
    );
};

export default Chatbot;
