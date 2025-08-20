import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BuildDetails from './pages/BuildDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/build/:id" element={<BuildDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
