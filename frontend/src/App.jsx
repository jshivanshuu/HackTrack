import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, AlertTriangle, Shield, TerminalSquare, LayoutDashboard, List } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const API_BASE = 'http://localhost:8000/api/v1/dashboard'; // Adjust to 8080 if you switched ports!

function App() {
    const [stats, setStats] = useState({ total_requests: 0, total_threats: 0, threats_by_type: [] });
    const [timeline, setTimeline] = useState([]);
    const [activeTab, setActiveTab] = useState('dashboard');

    const fetchData = async () => {
        try {
            const statsRes = await axios.get(`${API_BASE}/stats`);
            const timelineRes = await axios.get(`${API_BASE}/timeline`);
            setStats(statsRes.data);
            setTimeline(timelineRes.data);
        } catch (err) {
            console.error('Failed to load dashboard data', err);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 3000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="min-h-screen bg-background text-textMain">
            {/* Top Navbar */}
            <header className="sticky top-0 z-50 bg-card border-b border-gray-800 px-6 py-4 flex items-center justify-between shadow-md">
                <div className="flex items-center space-x-3">
                    <Shield className="h-8 w-8 text-primary" />
                    <h1 className="text-2xl font-bold tracking-tight text-white mr-8">HackTrack</h1>

                    <nav className="hidden md:flex space-x-1">
                        <button
                            onClick={() => setActiveTab('dashboard')}
                            className={`flex items-center px-4 py-2 rounded-md transition-colors font-medium text-sm ${activeTab === 'dashboard' ? 'bg-gray-800 text-white' : 'text-textMuted hover:text-white hover:bg-gray-800/50'}`}
                        >
                            <LayoutDashboard className="w-4 h-4 mr-2" /> Overview
                        </button>
                        <button
                            onClick={() => setActiveTab('feed')}
                            className={`flex items-center px-4 py-2 rounded-md transition-colors font-medium text-sm ${activeTab === 'feed' ? 'bg-gray-800 text-white' : 'text-textMuted hover:text-white hover:bg-gray-800/50'}`}
                        >
                            <List className="w-4 h-4 mr-2" /> Live Threats
                        </button>
                    </nav>
                </div>

                <div className="flex items-center space-x-2 text-sm text-textMuted bg-gray-800/80 px-3 py-1.5 rounded-full border border-gray-700 shadow-inner">
                    <Activity className="h-4 w-4 text-green-400 animate-pulse" />
                    <span>System Active</span>
                </div>
            </header>

            <main className="p-6 max-w-7xl mx-auto mt-4 animate-fade-in">

                {/* DASHBOARD TAB */}
                {activeTab === 'dashboard' && (
                    <div className="space-y-8 fade-in">
                        {/* Top Stats */}
                        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                            <div className="glass-box p-6 transition-transform hover:translate-y-[-2px] hover:shadow-primary/20">
                                <div className="text-textMuted text-sm font-medium uppercase tracking-wider">Total Events</div>
                                <div className="mt-2 text-4xl font-bold text-white">{stats.total_requests}</div>
                            </div>
                            <div className="glass-box p-6 border-l-4 border-l-threatHigh transition-transform hover:translate-y-[-2px]">
                                <div className="text-textMuted text-sm font-medium uppercase tracking-wider">Threats Blocked</div>
                                <div className="mt-2 text-4xl font-bold text-threatHigh">{stats.total_threats}</div>
                            </div>
                            {stats.threats_by_type.map((t) => (
                                <div key={t.name} className="glass-box p-6 transition-transform hover:translate-y-[-2px]">
                                    <div className="text-textMuted text-sm font-medium uppercase tracking-wider">{t.name} Detected</div>
                                    <div className="mt-2 text-4xl font-bold text-threatMedium">{t.value}</div>
                                </div>
                            ))}
                        </div>

                        {/* Chart Area */}
                        <div className="glass-box p-6 h-[400px]">
                            <h2 className="text-xl font-semibold mb-6 flex items-center text-white">
                                <Activity className="w-5 h-5 mr-2 text-primary" /> Active Threat Timeline
                            </h2>
                            <div className="w-full h-[85%]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={stats.threats_by_type}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
                                        <XAxis dataKey="name" stroke="#9ca3af" axisLine={false} tickLine={false} dy={10} />
                                        <YAxis stroke="#9ca3af" axisLine={false} tickLine={false} dx={-10} />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#151C2C', borderColor: '#1f2937', color: '#fff', borderRadius: '0.5rem', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }}
                                            itemStyle={{ color: '#ef4444', fontWeight: 'bold' }}
                                        />
                                        <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={4} dot={{ r: 5, fill: '#151C2C', strokeWidth: 2 }} activeDot={{ r: 8, fill: '#3B82F6' }} animationDuration={1500} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                )}

                {/* THREAT FEED TAB */}
                {activeTab === 'feed' && (
                    <div className="glass-box p-6 h-[75vh] flex flex-col fade-in">
                        <div className="flex items-center justify-between border-b border-gray-800 pb-4 mb-6">
                            <h2 className="text-xl font-semibold flex items-center text-white">
                                <TerminalSquare className="w-5 h-5 mr-2 text-secondary" /> Live Diagnostics
                            </h2>
                            <span className="text-xs font-mono text-gray-500 tracking-widest uppercase">Listening securely</span>
                        </div>

                        <div className="flex-1 overflow-y-auto space-y-4 pr-4 custom-scrollbar">
                            {timeline.length === 0 ? (
                                <div className="flex flex-col items-center justify-center h-full text-textMuted opacity-50">
                                    <Shield className="w-16 h-16 mb-4" />
                                    <p>No recent threats detected on the network.</p>
                                </div>
                            ) : (
                                timeline.map((threat, idx) => (
                                    <div key={threat.id} className="bg-[#0B0F19] rounded-xl p-5 border border-gray-800 hover:border-gray-600 transition-all duration-300 shadow-md">
                                        <div className="flex justify-between items-start mb-3">
                                            <div className="flex items-center space-x-3">
                                                <span className="bg-red-900/30 text-red-500 px-3 py-1 rounded-md font-mono text-sm tracking-wide border border-red-800/50 flex items-center">
                                                    <AlertTriangle className="w-3 h-3 mr-1.5" />
                                                    {threat.threat_type}
                                                </span>
                                                <span className="text-gray-500 text-sm font-medium">#{threat.id}</span>
                                            </div>
                                            <span className="text-gray-400 text-xs font-mono bg-gray-800/50 px-2 py-1 rounded">
                                                {new Date(threat.timestamp).toLocaleTimeString()}
                                            </span>
                                        </div>
                                        <div className="text-sm border-b border-gray-800 pb-3 mb-3">
                                            <span className="text-gray-400">Targeting route </span>
                                            <span className="text-secondary font-mono tracking-tight">{threat.endpoint}</span>
                                            <span className="text-gray-400 ml-2">from origin </span>
                                            <span className="text-primary font-mono tracking-tight">{threat.ip_address}</span>
                                        </div>
                                        <div className="text-sm text-gray-300 leading-relaxed bg-[#151C2C] p-3 rounded-lg flex items-start border border-gray-800/50 shadow-inner">
                                            <div className="mr-3 mt-0.5 text-blue-400">
                                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z" /></svg>
                                            </div>
                                            <span className="font-mono text-xs">{threat.ai_analysis || "Awaiting advanced deep scrutiny..."}</span>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
