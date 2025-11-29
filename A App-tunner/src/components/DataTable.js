import Table from 'react-bootstrap/Table';
import '../style/DataTable.css';

const DataTable = ({ table }) => {
    // check if there is any jobs have been process
    if (!table || table.length === 0){
        return(
            // display this message is there is on job processed
            <p className='text-center fs-1 fw-medium text-decoration-underline'>
                No data available!
            </p>
        );
    }

    // use to refresh the leaderboard
    const cleanData = table.map((item) =>({
        id: item._id$oid, // use mongo's object ID
        epochs: item.epochs, 
        learning_rate: item.learning_rate,
        batch_size: item.batch_size,
        accurarcy: item.accuracy,
        run_time: item.run_time,
    }));

    // a function that CSS class name depending on row's index
    const getRowClass = (index) => {
        switch(index){
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

    return(
        <div>
            <p className='title'>Top job configurations</p>
            <Table bordered hover>
                <thread>
                    <tr>
                        <th>Epochs</th>
                        <th>Learning Rate</th>
                        <th>Batch Size</th>
                        <th>Accuracy (%)</th>
                        <th>Run Time (seconds)</th>
                    </tr>
                </thread>
                <tbody>
                    {cleanData.map((row, index) => {
                        <tr key={row.id}>
                            <td className={getRowClass(index)}>{row.epochs}</td>
                            <td className={getRowClass(index)}>{row.learning_rate}</td>
                            <td className={getRowClass(index)}>{row.batch_size}</td>
                            <td className={getRowClass(index)}>{row.accuracy}</td>
                            <td className={getRowClass(index)}>{row.run_time}</td>
                        </tr>
                    })}
                </tbody>
            </Table>
        </div>
    )
};

export default DataTable;