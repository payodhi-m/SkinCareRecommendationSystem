import './chatBot.css';
import React, { useEffect, useState } from 'react';
import { IoMdSend } from 'react-icons/io';
import { BiBot, BiUser } from 'react-icons/bi';

function Basic() {
    const [chat, setChat] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [botTyping, setBotTyping] = useState(false);
    const [userName, setUserName] = useState('');  // Added state for user name

    useEffect(() => {
        const objDiv = document.getElementById('messageArea');
        objDiv.scrollTop = objDiv.scrollHeight;
    }, [chat]);

    const handleSubmit = (evt) => {
        evt.preventDefault();

        if (!userName) {
            alert("Please enter your name.");
            return;
        }

        const request_temp = { sender: "user", sender_id: userName, msg: inputMessage };

        if (inputMessage !== "") {
            setChat(chat => [...chat, request_temp]);
            setBotTyping(true);
            setInputMessage('');
            rasaAPI(userName, inputMessage);
        } else {
            window.alert("Please enter a valid message");
        }
    };

    const rasaAPI = async (name, msg) => {
        await fetch('http://localhost:5005/webhooks/rest/webhook', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "sender": name, "message": msg }),
        })
            .then(response => response.json())
            .then((response) => {
                if (response) {
                    const temp = response[0];
                    const recipient_msg = temp["text"];
                    const response_temp = { sender: "bot", msg: recipient_msg };
                    setBotTyping(false);
                    setChat(chat => [...chat, response_temp]);
                }
            });
    };

    const styles = {
        container: {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh',
            padding: '20px',
            background: 'linear-gradient(135deg, #1f1c3c, #3a3d7a)',
            boxSizing: 'border-box',
        },
        card: {
            width: '100%',
            maxWidth: '500px',
            background: 'rgba(255, 255, 255, 0.9)',
            borderRadius: '20px',
            boxShadow: '0px 8px 30px rgba(0, 0, 0, 0.2)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            boxSizing: 'border-box',
        },
        header: {
            padding: '20px',
            backgroundColor: '#6a5acd',
            color: 'black',
            textAlign: 'center',
            fontSize: '26px',
            fontWeight: 'bold',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
        },
        messageArea: {
            padding: '20px',
            height: '350px',
            overflowY: 'auto',
            backgroundColor: '#f3f4f6',
            scrollbarWidth: 'thin',
            borderBottom: '1px solid #ddd',
            boxSizing: 'border-box',
        },
        botMessage: {
            display: 'flex',
            alignItems: 'center',
            padding: '12px 16px',
            margin: '12px 0',
            backgroundColor: '#d0d1ff',
            borderRadius: '15px',
            color: '#333',
            maxWidth: '75%',
            alignSelf: 'flex-start',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        },
        userMessage: {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            padding: '12px 16px',
            margin: '12px 0',
            backgroundColor: '#6a5acd',
            color: 'white',
            borderRadius: '15px',
            maxWidth: '75%',
            alignSelf: 'flex-end',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        },
        footer: {
            display: 'flex',
            padding: '15px',
            backgroundColor: '#6a5acd',
            borderRadius: '0 0 20px 20px',
        },
        input: {
            flex: '1',
            padding: '12px 18px',
            borderRadius: '30px',
            border: '1px solid #ddd',
            outline: 'none',
            fontSize: '16px',
            boxShadow: '0px 0px 10px rgba(106, 90, 205, 0.2)',
            transition: 'box-shadow 0.3s ease',
        },
        sendButton: {
            background: 'linear-gradient(90deg, #8e8cff, #b080ff)',
            color: 'black',
            borderRadius: '50%',
            padding: '12px',
            border: 'none',
            cursor: 'pointer',
            marginLeft: '10px',
            boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.15)',
            transition: 'transform 0.2s, box-shadow 0.2s',
        },
        sendButtonHover: {
            transform: 'scale(1.1)',
            boxShadow: '0px 6px 15px rgba(0, 0, 0, 0.2)',
        },
    };

    const [sendButtonHover, setSendButtonHover] = useState(false);

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <div style={styles.header}>
                    Skincare AI Assistant
                    {botTyping && <h6>Bot Typing...</h6>}
                </div>
                <div style={styles.messageArea} id="messageArea">
                    {chat.map((message, index) => (
                        <div key={index} style={message.sender === 'bot' ? styles.botMessage : styles.userMessage}>
                            {message.sender === 'bot' ? <BiBot style={{ marginRight: '8px' }} /> : <BiUser style={{ marginLeft: '8px' }} />}
                            <span>{message.msg}</span>
                        </div>
                    ))}
                </div>
                <div style={styles.footer}>
                    <form style={{ display: 'flex', width: '100%' }} onSubmit={handleSubmit}>
                        <input
                            type="text"
                            style={styles.input}
                            placeholder="Type a message..."
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                        />
                        <button
                            type="submit"
                            style={sendButtonHover ? { ...styles.sendButton, ...styles.sendButtonHover } : styles.sendButton}
                            onMouseEnter={() => setSendButtonHover(true)}
                            onMouseLeave={() => setSendButtonHover(false)}
                        >
                            <IoMdSend />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Basic;
