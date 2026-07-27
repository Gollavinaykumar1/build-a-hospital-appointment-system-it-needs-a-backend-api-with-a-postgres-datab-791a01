# LLM Output

=== FILE: src/App.jsx ===
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { HashRouter, Route, Routes, useNavigate } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Calendar, Clock, User, Briefcase, Plus } from 'lucide-react';
import { format } from 'date-fns';
import { useForm } from 'react-hook-form';
import clsx from 'clsx';
import './App.css';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = {
  getItems: async () => {
    try {
      const response = await fetch(`${BASE_URL}/appointments`);
      const data = await response.json();
      return Array.isArray(data) ? data : (data?.items || []);
    } catch (error) {
      console.error(error);
      return [];
    }
  },
  createItem: async (item) => {
    try {
      const response = await fetch(`${BASE_URL}/appointments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      return null;
    }
  },
  updateItem: async (id, item) => {
    try {
      const response = await fetch(`${BASE_URL}/appointments/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      return null;
    }
  },
  deleteItem: async (id) => {
    try {
      const response = await fetch(`${BASE_URL}/appointments/${id}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      return null;
    }
  }
};

const Header = () => {
  const navigate = useNavigate();
  return (
    <header className="bg-gray-900 py-4">
      <nav className="container mx-auto flex justify-between">
        <h1 className="text-lg font-bold text-white">Hospital Appointment System</h1>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={() => navigate('/book-appointment')}>Book Appointment</button>
      </nav>
    </header>
  );
};

const Footer = () => {
  return (
    <footer className="bg-gray-900 py-4 mt-4">
      <p className="container mx-auto text-center text-white">&copy; 2024 Hospital Appointment System</p>
    </footer>
  );
};

const AppointmentList = () => {
  const [appointments, setAppointments] = useState([]);
  const [filter, setFilter] = useState('All');
  const [status, setStatus] = useState('All');

  const fetchAppointments = useCallback(async () => {
    const data = await api.getItems();
    setAppointments(data);
  }, []);

  useEffect(() => {
    fetchAppointments();
  }, [fetchAppointments]);

  const filteredAppointments = appointments.filter((appointment) => {
    if (filter === 'All') return true;
    return appointment.department === filter;
  }).filter((appointment) => {
    if (status === 'All') return true;
    return appointment.status === status;
  });

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-lg font-bold mb-4">Appointments</h2>
      <div className="flex justify-between mb-4">
        <select className="bg-gray-100 py-2 px-4 rounded" value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="All">All</option>
          <option value="General">General</option>
          <option value="Cardiology">Cardiology</option>
          <option value="Neurology">Neurology</option>
          <option value="Orthopedics">Orthopedics</option>
          <option value="Pediatrics">Pediatrics</option>
        </select>
        <select className="bg-gray-100 py-2 px-4 rounded" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="All">All</option>
          <option value="Scheduled">Scheduled</option>
          <option value="Pending">Pending</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>
      <table className="w-full table-auto">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2">Doctor Name</th>
            <th className="px-4 py-2">Department</th>
            <th className="px-4 py-2">Date/Time</th>
            <th className="px-4 py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {filteredAppointments.map((appointment) => (
            <tr key={appointment.id} className="bg-white hover:bg-gray-100">
              <td className="px-4 py-2">{appointment.doctorName}</td>
              <td className="px-4 py-2">{appointment.department}</td>
              <td className="px-4 py-2">{format(new Date(appointment.dateTime), 'yyyy-MM-dd HH:mm')}</td>
              <td className="px-4 py-2">
                <span className={clsx('py-1 px-2 rounded', {
                  'bg-green-200 text-green-600': appointment.status === 'Scheduled',
                  'bg-yellow-200 text-yellow-600': appointment.status === 'Pending',
                  'bg-red-200 text-red-600': appointment.status === 'Cancelled'
                })}>{appointment.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const BookAppointmentForm = () => {
  const { register, handleSubmit, reset } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const appointment = await api.createItem(data);
      if (appointment) {
        toast.success('Appointment booked successfully!');
        reset();
        navigate('/appointments');
      } else {
        toast.error('Failed to book appointment!');
      }
    } catch (error) {
      console.error(error);
      toast.error('Failed to book appointment!');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-lg font-bold mb-4">Book Appointment</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="patientName">Patient Name</label>
          <input className="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" id="patientName" {...register('patientName')} />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="doctor">Doctor</label>
          <select className="bg-gray-100 py-2 px-4 rounded" id="doctor" {...register('doctor')}>
            <option value="Dr. John Doe">Dr. John Doe</option>
            <option value="Dr. Jane Doe">Dr. Jane Doe</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="department">Department</label>
          <select className="bg-gray-100 py-2 px-4 rounded" id="department" {...register('department')}>
            <option value="General">General</option>
            <option value="Cardiology">Cardiology</option>
            <option value="Neurology">Neurology</option>
            <option value="Orthopedics">Orthopedics</option>
            <option value="Pediatrics">Pediatrics</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="dateTime">Date/Time</label>
          <input className="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="datetime-local" id="dateTime" {...register('dateTime')} />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="notes">Notes</label>
          <textarea className="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="notes" {...register('notes')} />
        </div>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit">Book Appointment</button>
      </form>
    </div>
  );
};

const App = () => {
  return (
    <HashRouter>
      <Header />
      <Routes>
        <Route path="/" element={<AppointmentList />} />
        <Route path="/appointments" element={<AppointmentList />} />
        <Route path="/book-appointment" element={<BookAppointmentForm />} />
      </Routes>
      <Footer />
      <ToastContainer />
    </HashRouter>
  );
};

export default App;
=== END ===