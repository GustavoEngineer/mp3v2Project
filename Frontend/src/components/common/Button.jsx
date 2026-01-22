import React from 'react';

const Button = ({ onClick, disabled, children, className = '' }) => {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`btn ${className}`}
            style={{
                padding: '0.6em 1.2em',
                fontSize: '1em',
                fontWeight: 500,
                fontFamily: 'inherit',
                cursor: disabled ? 'not-allowed' : 'pointer',
                opacity: disabled ? 0.6 : 1,
                transition: 'border-color 0.25s',
            }}
        >
            {children}
        </button>
    );
};

export default Button;
