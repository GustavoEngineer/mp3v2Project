import React from 'react';

const Input = ({ type = 'text', placeholder, value, onChange, className = '' }) => {
    return (
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            className={`input ${className}`}
            style={{
                padding: '10px',
                width: '100%',
                maxWidth: '500px',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '1rem',
            }}
        />
    );
};

export default Input;
