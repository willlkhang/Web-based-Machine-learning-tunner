import React from 'react';
import Table from 'react-bootstrap/Table';
import '../style/LeadBoard.css';

const LeadBoard = ({ table }) => {
	if (!table || table.length === 0) {
		return (
			<p className='text-center fs-1 fw-medium text-decoration-underline'>
				No Traning available!
			</p>
		);
	}

	const cleanData = table.map((item) => ({
		id: item._id.$oid,
		epochs: item.epochs,
		learning_rate: item.learning_rate,
		batch_size: item.batch_size,
		accuracy: item.accuracy,
		run_time: item.run_time,
	}));

	const getRowClass = (index) => {
		switch (index) {
			case 0:
				return 'gold';
			case 1:
				return 'silver';
			case 2:
				return 'bronze';
			default:
				return '';
		}
	};

	return (
		<div className='leadboard h-100 d-inline-block w-100 p-3 border border-'>
			<div>
				<p className='title pt-5'>Top Model Architecture Hyperparameters configurations</p>
				<Table bordered hover>
					<thead>
						<tr>
							<th>Epochs</th>
							<th>Learning Rate</th>
							<th>Batch Size</th>
							<th>Accuracy (%)</th>
							<th>Run Time (seconds)</th>
						</tr>
					</thead>
					<tbody>
						{cleanData.map((row, index) => (
							<tr key={row.id}>
								<td className={getRowClass(index)}>{row.epochs}</td>
								<td className={getRowClass(index)}>{row.learning_rate}</td>
								<td className={getRowClass(index)}>{row.batch_size}</td>
								<td className={getRowClass(index)}>{row.accuracy}</td>
								<td className={getRowClass(index)}>{row.run_time}</td>
							</tr>
						))}
					</tbody>
				</Table>
			</div>
		</div>
	);
};

export default LeadBoard;