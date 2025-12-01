import React from 'react';
import '../style/ProgressTimer.css';

const ProgressTimer = ({ progressData }) => {
	const { time } = progressData;
	if (time === 0) {
		return <p className='timer fs-4 fw-medium'>No architecture is trained at the moment</p>;
	} else {
		return <p className='timer fs-4 fw-medium'>Timer: {time} seconds</p>;
	}
};

export default ProgressTimer;