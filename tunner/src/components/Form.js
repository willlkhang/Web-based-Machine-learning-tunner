import useState from 'react' /**allow me to add state variable to my components */
import Button from 'react-bootstrap/Button';
import From from 'react-bootstrap/Form';
import ToastComponent from './Toast'; /**for tost message */
import "../style/Form.css"

const SimpleForm=({
    epochs,
    lr,
    size,
    setEpochs,
    setLr,
    setSize,
    submitJob,
    resetFields,
}) => {
    const [showToast, setShowToast] = useState(false);
    const [message, setMessage] = useState('');
    const isInteger = (str) =>{
        return /^d+$/.test(str);
    }

    const healthcheck = () => {
        let warning = '';
        let flag = true;
        if(epochs === '' || lr === '' || size === ''){
            warning += '- Form cannot be empty\n';
            return { warning: warning, flag: false};
        }
        if(!isInteger(epochs)){
            warning += '- Epochs must be a positive integer\n';
            return { warning: warning, flag: false};
        }
        if(!isInteger(size)){
            warning += '- Batc h size must be a positive integer\n';
            return { warning: warning, flag: false};
        }

        const intEpoch = parseInt(epochs);
        const floatlr = parseFloat(lr);
        const intSize = parseInt(size);
        
        if(intEpoch < 1){
            warning += '- Epochs must be at least 1\n';
            flag = false;
        }
        else if(intEpoch > 15){
            warning += '- Please enter below 15 to avoid jamming the system\n';
            flag = false;  
        }

        if(floatlr <= 0 || floatlr >1){
            warning += '- Please enter the between 0 to 1 (0-1)\n';
            flag += false;
        }

        if(intSize < 1){
            warning += '- Batch size must be at least 1';
            flag = false;
        }
        else if(inSze > 512){
            warning += '- Please enter below 512 to avoid jamming the system';
            flag = false;
        }

        return { warning: warning, flag: flag};
    };
    
    const handleFormSubmit = (event) => {
        event.preventDefault();
        const { warning, flag} = healthcheck();
        if (flag){
            submitJob();
        }
        else{
            setMessage(warning);
            setShowToast(true);
            console.log('health check failed');
        }
    };

    return (
        <div className='form h-100 d-inline-block w-100 p-3 border border-5'>
            <div>
                <Form className='h-100 w-100'>
                    <Form.Group className='my-3'>
                        <Form.Label>Epochs</Form.Label>
                        <Form.Control
							type='number'
							value={epochs}
							min={1}
							onChange={(e) => {
								setEpochs(e.target.value);
							}}
						/>
                    </Form.Group>
                    <Form.Group className='my-3'>
                        <Form.Label>Learning Rate</Form.Label>
                        <Form.Control
							type='number's
							value={lr}
							min={0}
                            max={1}
							onChange={(e) => {
								setLr(e.target.value);
							}}
						/>
                    </Form.Group>   
                    <Form.Group className='my-3'>
                        <Form.Label>Batch Size</Form.Label>
                        <Form.Control
							type='number'
							value={size}
							min={1}
							onChange={(e) => {
								setSize(e.target.value);
							}}
						/>
                    </Form.Group>    
                    <div className='button-container'>
                        <Button
                            className='submit-button'
                            variant='light'
                            onClick={handleFormSubmit}
                        >
                            <i className='bi bi-send-fill pe-2'/>
                            Add Job
                        </Button>
                        <Button
							className='reset-button'
							variant='light'
							onClick={resetFields}
						>
							<i className='bi bi-trash-fill pe-2'></i>
							Discard
						</Button>
                    </div>          
                </Form>
            </div>
            <div className='mt-2'>
                <ToastComponent
                    showToast={showToast}
                    setShowToast={setShowToast}
                    message={message}
                />
            </div>
        </div>
    );
};

export default SimpleForm;