import React from 'react'
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import TemperatureTable from './TemperatureTable';
import Chip from '@material-ui/core/Chip';

class AccordionTemps extends React.Component {

    constructor(props) {
        super(props);
    }

    display() {
        return this.props.temps.length > 0 && this.props.hour <= new Date().getHours()

    }

    firstItem() {
        return this.props.temps[this.props.temps.length - 1]
    }

    avg(){
        let avgTemp=0
        let avgHum=0
        for(let temp in this.props.temps ){
            avgTemp+=this.props.temps[temp].temp
            avgHum+=this.props.temps[temp].humidity
        }
        return {
            temp: avgTemp/this.props.temps.length,
            humidity: avgHum/this.props.temps.length
        }
    }




    render() {

        if (this.display())

            return (

                <div>
                    <Accordion>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel1a-content"
                            id="panel1a-header"
                        >
                                    <Chip
                                        label={this.props.hour+":00h"}
                                    />
                                    <Chip
                                        color="secondary"
                                        label={this.firstItem().temp.toFixed(2) + "ºC"}
                                    />
                                    <Chip
                                        color="primary"
                                        label={this.firstItem().humidity.toFixed(2) + "%"}
                                    />
               
                        </AccordionSummary>
                        <AccordionDetails style={{flexDirection:"column"}}>
                            <Chip 
                            variant="outlined"
                            color="primary"
                            label={"Temp media "+ this.avg().temp.toFixed(2)+"ºC Humedad media "+ this.avg().humidity.toFixed(2)+"%"}></Chip>
                            <br /><TemperatureTable temps={this.props.temps}></TemperatureTable>
                        </AccordionDetails>
                    </Accordion>
                </div>
            )
        else return ""

    }
}
export default AccordionTemps