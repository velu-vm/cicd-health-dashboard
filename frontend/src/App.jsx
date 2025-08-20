import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BuildDetails from './pages/BuildDetails';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/build/:id" element={<BuildDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
