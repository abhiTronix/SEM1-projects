import React, { Component } from 'react';

// Spinner Component
export class Spinner extends Component {
    render() {
        return (
            <div className="text-center">
                <div className="spinner-border text-primary mySpinner" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        )
    }
}

export default Spinner
