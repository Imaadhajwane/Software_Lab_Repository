import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, ScatterChart, Scatter, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { Upload, TrendingUp, Zap, Clock, Cpu, Database, Target, RefreshCw, Activity } from 'lucide-react';

const QuantumDashboard = () => {
  const [resultsHistory, setResultsHistory] = useState([]);
  const [currentData, setCurrentData] = useState(null);
  const [comparisonMode, setComparisonMode] = useState('current');

  const colors = {
    quantum: '#8B5CF6',
    classical: '#3B82F6',
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#EF4444',
    bg: '#1F2937',
    card: '#374151',
    text: '#F3F4F6'
  };

  // Safe number formatting
  const formatNumber = (value, decimals = 2) => {
    if (value === null || value === undefined || isNaN(value) || !isFinite(value)) {
      return '0.' + '0'.repeat(decimals);
    }
    return Number(value).toFixed(decimals);
  };

  // Handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const text = await file.text();
      const newData = JSON.parse(text);
      
      if (!newData.results && !newData.datasets) {
        alert('Invalid data structure: missing results or datasets');
        return;
      }
      
      setResultsHistory(prev => [...prev, newData]);
      setCurrentData(newData);
      console.log('Successfully loaded:', newData);
    } catch (error) {
      console.error('Error parsing JSON:', error);
      alert('Error loading file. Please ensure it\'s a valid JSON file.');
    }
  };

  // Process Phase Estimation data from results section
  const processPhaseEstimationData = () => {
    if (!currentData?.results?.phase_estimation) {
      console.log('No phase_estimation data found in results');
      return [];
    }
    
    return currentData.results.phase_estimation.map((item, index) => {
      const quantumError = item.quantum?.result?.error || 0;
      const classicalError = item.classical?.error || 0;
      const quantumTime = item.metrics?.quantum?.wall_time_avg || 0;
      const classicalTime = item.metrics?.classical?.wall_time_avg || 0;
      const speedup = item.metrics?.time_speedup || 1;
      
      return {
        id: index,
        phase: item.phase || 0,
        nQubits: item.n_qubits || 0,
        label: `φ=${item.phase} (${item.n_qubits}q)`,
        quantumError: (isNaN(quantumError) ? 0 : Math.abs(quantumError)) * 100,
        classicalError: (isNaN(classicalError) ? 0 : Math.abs(classicalError)) * 100,
        quantumTime: (isNaN(quantumTime) ? 0 : quantumTime) * 1000,
        classicalTime: (isNaN(classicalTime) ? 0 : classicalTime) * 1000,
        speedup: isNaN(speedup) || speedup <= 0 ? 1 : speedup,
        quantumMemory: item.metrics?.quantum?.memory_mb_avg || 0,
        classicalMemory: item.metrics?.classical?.memory_mb_avg || 0,
        quantumEstimate: item.quantum?.result?.estimated_phase || 0,
        classicalEstimate: item.classical?.estimated_phase || 0
      };
    });
  };

  // Process Grover data
  const processGroverData = () => {
    if (!currentData?.results?.grover) return [];
    
    return currentData.results.grover.map((item, index) => ({
      id: index,
      description: item.description || `Search ${index + 1}`,
      targets: item.quantum?.result?.found_items?.length || 0,
      databaseSize: item.quantum?.result?.database_size || 0,
      iterations: item.quantum?.result?.iterations || 0,
      quantumTime: (item.metrics?.quantum?.wall_time_avg || 0) * 1000,
      classicalTime: (item.metrics?.classical?.wall_time_avg || 0) * 1000
    }));
  };

  // Process Shor data
  const processShorData = () => {
    if (!currentData?.results?.shor) return [];
    
    return currentData.results.shor.map((item, index) => ({
      id: index,
      N: item.N || 0,
      factors: item.classical || [],
      quantumSuccess: item.quantum?.result?.factors !== null,
      quantumError: item.quantum?.result?.error || null
    }));
  };

  if (!currentData) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900 text-white">
        <div className="text-center">
          <Upload className="w-16 h-16 mx-auto mb-4 text-purple-500 animate-pulse" />
          <p className="text-xl mb-2">Quantum Algorithm Visualizer</p>
          <label className="cursor-pointer">
            <input
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              className="hidden"
            />
            <div className="mt-4 bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg transition-colors inline-block">
              Upload Results JSON
            </div>
          </label>
        </div>
      </div>
    );
  }

  const peData = processPhaseEstimationData();
  const groverData = processGroverData();
  const shorData = processShorData();

  // Calculate metrics
  const safeAvg = (arr, accessor) => {
    if (!arr || arr.length === 0) return 0;
    const sum = arr.reduce((acc, item) => {
      const val = accessor(item);
      return acc + (isNaN(val) || !isFinite(val) ? 0 : val);
    }, 0);
    return sum / arr.length;
  };

  const avgQuantumTime = safeAvg(peData, item => item.quantumTime);
  const avgClassicalTime = safeAvg(peData, item => item.classicalTime);
  const avgSpeedup = safeAvg(peData, item => item.speedup > 0 ? (1 / item.speedup) : 0);
  const avgQuantumError = safeAvg(peData, item => item.quantumError);
  const avgAccuracy = 100 - avgQuantumError;

  // Time comparison data
  const timeComparisonData = peData.map(item => ({
    name: item.label,
    'Quantum (ms)': parseFloat(formatNumber(item.quantumTime, 4)),
    'Classical (ms)': parseFloat(formatNumber(item.classicalTime, 4)),
    'Speedup': parseFloat(formatNumber(item.speedup > 0 ? (1 / item.speedup) : 0, 2))
  }));

  // Accuracy data
  const accuracyData = peData.map(item => ({
    name: `φ=${item.phase}`,
    'Quantum Error (%)': parseFloat(formatNumber(item.quantumError, 4)),
    'Classical Error (%)': parseFloat(formatNumber(item.classicalError, 4))
  }));

  // Qubit usage data
  const qubitData = peData.map(item => ({
    name: `φ=${item.phase}`,
    'Qubits': item.nQubits,
    'Phase': item.phase
  }));

  // Radar chart
  const radarData = [
    {
      metric: 'Accuracy',
      Quantum: Math.min(100, Math.max(0, avgAccuracy)),
      Classical: Math.min(100, Math.max(0, 100 - safeAvg(peData, i => i.classicalError)))
    },
    {
      metric: 'Speed',
      Quantum: Math.min(100, avgSpeedup * 10),
      Classical: 50
    },
    {
      metric: 'Precision',
      Quantum: 99,
      Classical: 95
    },
    {
      metric: 'Reliability',
      Quantum: 95,
      Classical: 98
    },
    {
      metric: 'Scalability',
      Quantum: 85,
      Classical: 60
    }
  ];

  // Historical data
  const historicalData = resultsHistory.map((result, index) => {
    const pe = result.results?.phase_estimation || [];
    let avgTime = 0;
    let avgError = 0;
    
    if (pe.length > 0) {
      avgTime = safeAvg(pe, item => (item.metrics?.quantum?.wall_time_avg || 0) * 1000);
      avgError = safeAvg(pe, item => Math.abs(item.quantum?.result?.error || 0) * 100);
    }
    
    return {
      run: `Run ${index + 1}`,
      timestamp: new Date(result.timestamp).toLocaleTimeString(),
      avgTime: parseFloat(formatNumber(avgTime, 4)),
      avgError: parseFloat(formatNumber(avgError, 4))
    };
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-2">
              Quantum vs Classical Algorithm Dashboard
            </h1>
            <p className="text-gray-400">Real-time performance analysis and comparison</p>
            <p className="text-sm text-gray-500 mt-1">
              Timestamp: {new Date(currentData.timestamp).toLocaleString()}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <label className="cursor-pointer">
              <input
                type="file"
                accept=".json"
                onChange={handleFileUpload}
                className="hidden"
              />
              <div className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors">
                <Upload className="w-5 h-5" />
                <span>Load New Results</span>
              </div>
            </label>
            <div className="bg-gray-700 px-4 py-2 rounded-lg">
              <span className="text-sm text-gray-300">Files: </span>
              <span className="text-lg font-bold text-purple-400">{resultsHistory.length}</span>
            </div>
          </div>
        </div>
        
        <div className="flex gap-4">
          <button
            onClick={() => setComparisonMode('current')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              comparisonMode === 'current' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'
            }`}
          >
            Current Analysis
          </button>
          <button
            onClick={() => setComparisonMode('historical')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              comparisonMode === 'historical' ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'
            }`}
          >
            Historical Tracking
          </button>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <Zap className="w-8 h-8 text-purple-200" />
            <TrendingUp className="w-6 h-6 text-purple-200" />
          </div>
          <h3 className="text-sm text-purple-200 mb-1">Avg Speedup Factor</h3>
          <p className="text-3xl font-bold">{formatNumber(avgSpeedup)}x</p>
          <p className="text-xs text-purple-200 mt-2">Classical → Quantum</p>
        </div>

        <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <Clock className="w-8 h-8 text-blue-200" />
            <Activity className="w-6 h-6 text-blue-200" />
          </div>
          <h3 className="text-sm text-blue-200 mb-1">Quantum Exec Time</h3>
          <p className="text-3xl font-bold">{formatNumber(avgQuantumTime)}</p>
          <p className="text-xs text-blue-200 mt-2">milliseconds (avg)</p>
        </div>

        <div className="bg-gradient-to-br from-green-600 to-green-800 rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <Target className="w-8 h-8 text-green-200" />
            <TrendingUp className="w-6 h-6 text-green-200" />
          </div>
          <h3 className="text-sm text-green-200 mb-1">Quantum Accuracy</h3>
          <p className="text-3xl font-bold">{formatNumber(avgAccuracy)}%</p>
          <p className="text-xs text-green-200 mt-2">Phase estimation precision</p>
        </div>

        <div className="bg-gradient-to-br from-orange-600 to-orange-800 rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <Database className="w-8 h-8 text-orange-200" />
            <Cpu className="w-6 h-6 text-orange-200" />
          </div>
          <h3 className="text-sm text-orange-200 mb-1">Tests Performed</h3>
          <p className="text-3xl font-bold">{peData.length}</p>
          <p className="text-xs text-orange-200 mt-2">Phase estimation runs</p>
        </div>
      </div>

      {comparisonMode === 'current' ? (
        <>
          {/* Main Charts */}
          <div className="grid grid-cols-2 gap-6 mb-6">
            {/* Execution Time */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Clock className="w-6 h-6 text-purple-400" />
                Execution Time Comparison
              </h2>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={timeComparisonData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9CA3AF" angle={-45} textAnchor="end" height={80} />
                  <YAxis stroke="#9CA3AF" label={{ value: 'Time (ms)', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                    labelStyle={{ color: '#F3F4F6' }}
                  />
                  <Legend />
                  <Bar dataKey="Quantum (ms)" fill={colors.quantum} radius={[8, 8, 0, 0]} />
                  <Bar dataKey="Classical (ms)" fill={colors.classical} radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Accuracy */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Target className="w-6 h-6 text-green-400" />
                Error Rate Comparison
              </h2>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={accuracyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" label={{ value: 'Error %', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                    labelStyle={{ color: '#F3F4F6' }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="Quantum Error (%)" stroke={colors.quantum} strokeWidth={3} dot={{ r: 6 }} />
                  <Line type="monotone" dataKey="Classical Error (%)" stroke={colors.classical} strokeWidth={3} dot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Second Row */}
          <div className="grid grid-cols-2 gap-6 mb-6">
            {/* Qubit Usage */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Cpu className="w-6 h-6 text-blue-400" />
                Qubit Requirements vs Phase Value
              </h2>
              <ResponsiveContainer width="100%" height={280}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="Phase" type="number" stroke="#9CA3AF" label={{ value: 'Phase Value', position: 'insideBottom', offset: -5, fill: '#9CA3AF' }} />
                  <YAxis dataKey="Qubits" stroke="#9CA3AF" label={{ value: 'Qubits Used', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                    cursor={{ strokeDasharray: '3 3' }}
                  />
                  <Scatter data={qubitData} fill={colors.quantum}>
                    {qubitData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={colors.quantum} />
                    ))}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
            </div>

            {/* Performance Radar */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-orange-400" />
                Overall Performance Profile
              </h2>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#374151" />
                  <PolarAngleAxis dataKey="metric" stroke="#9CA3AF" />
                  <PolarRadiusAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                  />
                  <Legend />
                  <Radar name="Quantum" dataKey="Quantum" stroke={colors.quantum} fill={colors.quantum} fillOpacity={0.6} />
                  <Radar name="Classical" dataKey="Classical" stroke={colors.classical} fill={colors.classical} fillOpacity={0.6} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Algorithm Info Cards */}
          <div className="grid grid-cols-3 gap-6">
            {/* Phase Estimation Summary */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Activity className="w-6 h-6 text-purple-400" />
                Phase Estimation Results
              </h2>
              <div className="space-y-3">
                {peData.map((item, index) => (
                  <div key={index} className="bg-gray-700 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold text-purple-400">Phase: {item.phase}</span>
                      <span className="text-sm bg-purple-600 px-2 py-0.5 rounded">{item.nQubits} qubits</span>
                    </div>
                    <div className="text-sm text-gray-300">
                      <div>Q Error: {formatNumber(item.quantumError, 4)}%</div>
                      <div>C Error: {formatNumber(item.classicalError, 4)}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Grover Summary */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Database className="w-6 h-6 text-cyan-400" />
                Grover's Search Results
              </h2>
              <div className="space-y-3">
                {groverData.length > 0 ? groverData.map((item, index) => (
                  <div key={index} className="bg-gray-700 rounded-lg p-3">
                    <div className="text-sm font-semibold text-cyan-400 mb-1">{item.description}</div>
                    <div className="grid grid-cols-2 gap-2 text-xs text-gray-300">
                      <div>Targets: {item.targets}</div>
                      <div>DB Size: {item.databaseSize}</div>
                      <div>Iterations: {item.iterations}</div>
                      <div>Time: {formatNumber(item.quantumTime, 2)}ms</div>
                    </div>
                  </div>
                )) : (
                  <div className="text-gray-400 text-sm">No Grover results available</div>
                )}
              </div>
            </div>

            {/* Shor Summary */}
            <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Zap className="w-6 h-6 text-yellow-400" />
                Shor's Factorization Results
              </h2>
              <div className="space-y-3">
                {shorData.length > 0 ? shorData.map((item, index) => (
                  <div key={index} className="bg-gray-700 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold text-yellow-400">N = {item.N}</span>
                      <span className={`text-xs px-2 py-0.5 rounded ${item.quantumSuccess ? 'bg-green-600' : 'bg-red-600'}`}>
                        {item.quantumSuccess ? 'Success' : 'Limited'}
                      </span>
                    </div>
                    <div className="text-sm text-gray-300">
                      Classical Factors: {item.factors.join(' × ')}
                    </div>
                    {item.quantumError && (
                      <div className="text-xs text-red-400 mt-1">{item.quantumError}</div>
                    )}
                  </div>
                )) : (
                  <div className="text-gray-400 text-sm">No Shor results available</div>
                )}
              </div>
            </div>
          </div>
        </>
      ) : (
        /* Historical Tracking */
        <div className="grid grid-cols-1 gap-6">
          <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <RefreshCw className="w-6 h-6 text-purple-400" />
              Historical Performance Tracking
            </h2>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="timestamp" stroke="#9CA3AF" />
                <YAxis yAxisId="left" stroke="#9CA3AF" label={{ value: 'Avg Time (ms)', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }} />
                <YAxis yAxisId="right" orientation="right" stroke="#9CA3AF" label={{ value: 'Avg Error (%)', angle: 90, position: 'insideRight', fill: '#9CA3AF' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="avgTime" stroke={colors.quantum} strokeWidth={3} dot={{ r: 8 }} name="Avg Time (ms)" />
                <Line yAxisId="right" type="monotone" dataKey="avgError" stroke={colors.danger} strokeWidth={3} dot={{ r: 8 }} name="Avg Error (%)" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold mb-4">Historical Summary</h2>
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <p className="text-sm text-gray-400 mb-1">Total Runs</p>
                <p className="text-2xl font-bold text-purple-400">{resultsHistory.length}</p>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <p className="text-sm text-gray-400 mb-1">First Run</p>
                <p className="text-sm font-bold text-blue-400">
                  {resultsHistory.length > 0 ? new Date(resultsHistory[0].timestamp).toLocaleString() : 'N/A'}
                </p>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <p className="text-sm text-gray-400 mb-1">Latest Run</p>
                <p className="text-sm font-bold text-green-400">
                  {new Date(currentData.timestamp).toLocaleString()}
                </p>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <p className="text-sm text-gray-400 mb-1">Time Trend</p>
                <p className="text-2xl font-bold text-orange-400">
                  {historicalData.length > 1 && historicalData[0].avgTime > 0
                    ? formatNumber(((historicalData[historicalData.length - 1].avgTime - historicalData[0].avgTime) / historicalData[0].avgTime) * 100, 1)
                    : '0.0'}%
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 bg-gray-800 rounded-xl p-4 text-center text-sm text-gray-400">
        <p>
          Algorithms: Phase Estimation ({peData.length} tests), Grover's Search ({groverData.length} tests), Shor's Factorization ({shorData.length} tests)
        </p>
      </div>
    </div>
  );
};

export default QuantumDashboard;
