import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css'

function App() {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/logs")
        setLogs(response.data)
      } catch (error) {
        console.error("Error fetching data:", error)
      }
    }

    fetchLogs()
    const interval = setInterval(fetchLogs, 2000)
    return () => clearInterval(interval)
  }, []) 

  // Format data for the graph
  const graphData = [...logs].reverse().map(log => ({
    ...log,
    time: new Date(log.timestamp).toLocaleTimeString()
  }))

  return (
    <div className="dashboard" style={{ padding: '20px', backgroundColor: '#222', minHeight: '100vh', color: 'white' }}>
      <h1>GridMon Dashboard (v1.0 AI)</h1>
      
      <div className="card" style={{ background: '#333', padding: '20px', borderRadius: '10px', marginTop: '20px' }}>
        <h2>Live System Performance</h2>
        
        <div style={{ width: '100%', height: 400 }}>
          <ResponsiveContainer>
            <LineChart data={graphData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis dataKey="time" stroke="#888" />
              <YAxis domain={[0, 100]} stroke="#888" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111', border: 'none' }}
                itemStyle={{ color: '#fff' }}
              />
              <Legend />
              {/* CPU Line (Purple) */}
              <Line type="monotone" dataKey="cpu_usage" stroke="#8884d8" strokeWidth={2} dot={false} name="CPU %" />
              
              {/* Memory Line (Green) */}
              <Line type="monotone" dataKey="memory_usage" stroke="#82ca9d" strokeWidth={2} dot={false} name="RAM %" />
              
              {/* NEW: Disk Line (Orange) */}
              <Line type="monotone" dataKey="disk_usage" stroke="#ff7300" strokeWidth={2} dot={false} name="DISK %" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default App