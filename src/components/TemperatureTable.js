import React from 'react'
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

class TemperatureTable  extends React.Component {

    constructor(props) {
        super(props);
    }
    render() {
        return (
            <TableContainer >
                <Table size="small" >
                    <TableHead>
                        <TableRow>
                            <TableCell>Fecha</TableCell>
                            <TableCell>Temperatura (ºC)</TableCell>
                            <TableCell>Humedad (%)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {this.props.temps.map((row) => (
                            <TableRow key={row.date}>
                                <TableCell component="th" scope="row">
                                    {new Date(row.date).toLocaleString()}
                                </TableCell>
                                <TableCell align="right">{row.temp.toFixed(2)} º C</TableCell>
                                <TableCell align="right">{row.humidity.toFixed(2)} %</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

        )
    }

}
export default TemperatureTable 