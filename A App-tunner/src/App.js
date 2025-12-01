import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import Header from './components/Header';
import Form from './components/Form';
import DataTable from './components/DataTable';
import ProgressBar from './components/ProgressBar';
import MessageBoard from './components/MessageBoard';
import ProgressTimer from './components/ProgressTimer';
import Icon from './components/Icon';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './App.css';

const BACKEND_API = `http://localhost:9000`
const socket = io(BACKEND_API); //Link to FLASK BACKEND

function App() {

	//initial states for all pramas
	const [progressData, setProgressData] = useState({
		time: 0,
		total_progress: 0,
	});

	const [epochs, setEpochs] = useState('');
	const [lr, setLr] = useState('');
	const [size, setSize] = useState('');
	const [table, setTable] = useState([]);
	const [messages, setMessages] = useState([]);
	const d = new Date();

	const getJobs = () => {
		const url = `${BACKEND_API}/get-job`;

		fetch(url)
			.then((response) => response.json()).then((data) => {

				const jsonData = JSON.parse(data.data);

				const formattedData = jsonData.map((item) => {
					const id = item._id.$oid; //fetch ID
					return { id, ...item }; //return new object
				});

				setTable(formattedData);
			})
			.catch((error) => console.error('Fetch error:', error));
	};

	const findJob = (params) => {
		const queryParams = new URLSearchParams(params).toString(); 

		const url = `${BACKEND_API}/find-job?${queryParams}`;

		const options = {
			method: 'GET',
		};

		fetch(url, options)
			.then((response) => response.json()).then((data) => {

				const job = JSON.parse(data.data);
				const messageContent = `Job configuration {epochs: ${job.epochs},`+ 
										`learning_rate: ${job.learning_rate},`+
										`batch_size: ${job.batch_size}} finished in ${job.run_time} seconds.`+ 
										`Calculated accuracy: ${job.accuracy}%`;
				const doneMessage = {
					time: d.toLocaleTimeString(),
					message: messageContent,
				};
				// Using setState's callback to ensure doneMessage is added after submitMessage
				setMessages((prevMessages) => {
					const newMessages = [doneMessage, ...prevMessages];
					return newMessages.slice(0, 10);
				});
			});
	};

	const submitJob = () => {

		const url = `${BACKEND_API}/create-job`;

		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json', //telling backend, slient is sending json
			},
			body: JSON.stringify({ //packing config in json string
				epochs: epochs,
				learning_rate: lr,
				batch_size: size,
			}),
		};

		fetch(url, options)
			.then((response) => response.json())
			.then((data) => {

				if (!data.data) {

					const errorMessage = {
						time: d.toLocaleTimeString(),
						message: `Error: ${data.message}`, // Show the backend error
					};

					setMessages((prevMessages) => [errorMessage, ...prevMessages]);
					return; // Stop here,
				}

				let messageContent = data.message;
				const job = JSON.parse(data.data);
				
				if (job !== null) {
					if (job.status === true) {
						// status only true if job is done + updated to table
						messageContent += ` Calculated accuracy: ${job.accuracy}%`;
					} else {
						messageContent += ` Job currently in queue waiting to be processed`;
					}

					const doneMessage = {
						time: d.toLocaleTimeString(),
						message: messageContent,
					};

					// Using setState's callback to ensure doneMessage is added after submitMessage
					setMessages((prevMessages) => {
						const newMessages = [doneMessage, ...prevMessages];
						return newMessages.slice(0, 10);
					});
				}
			});
	};

	useEffect(() => { //listener for event sent by backend

		const handleResponse = (data) => {
			const { time, total_progress } = data;
			setProgressData({
				time: parseFloat(time),
				total_progress: parseFloat(total_progress),
			});
		};

		const handleExperimentDone = (data) => {
			findJob(data);
			getJobs();
		};

		socket.on('response', handleResponse); //backend sends training process for the bar updates in real-time
		socket.on('experiment_done', handleExperimentDone); //update with accuracy

		getJobs();

		return () => { //close socket
			socket.off('response', handleResponse); 
			socket.off('experiment_done', handleExperimentDone);
		};
		
	}, []);

	const resetFields = () => {
		setEpochs('');
		setLr('');
		setSize('');
	};

	return (
		<div className='main-container'>
			<div className='top-container'>
				<div className='left-container'>
					<div className='header-container'>
						<div className='icon-comp'>
							<Icon />
						</div>
						<div className='header-comp'>
							<Header id='header' />
						</div>
					</div>
					<div className='form-container'>
						<div className='form-comp'>
							<Form
								epochs={epochs}
								lr={lr}
								size={size}
								setEpochs={setEpochs}
								setLr={setLr}
								setSize={setSize}
								submitJob={submitJob}
								resetFields={resetFields}
							/>
						</div>
					</div>
				</div>
				<div className='right-container'>
					<div className='message-board-container'>
						<div className='message-board-title'>
							<p className='fs-3 text-center w-100'>MESSAGE BOARD</p>
						</div>
						<div className='message-board-table mt-5'>
							<MessageBoard messages={messages}></MessageBoard>
						</div>
					</div>
					<div className='progress-bar-container'>
						<div className='progress-bar-timer-comp'>
							<ProgressTimer progressData={progressData} />
						</div>
						<div className='progress-bar-comp'>
							{/* <ProgressTimer progressData={progressData} /> */}
							<ProgressBar progressData={progressData} />
						</div>
					</div>
				</div>
			</div>
			
			<div className='bottom-container'>
				<div className='job-board-comp'>
					<DataTable table={table} />
				</div>
			</div>
		</div>
	);
}

export default App;