import React from 'react'
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import Icon from '@material-ui/core/Icon'
import Paper from '@material-ui/core/Paper';
import Battery20Icon from '@material-ui/icons/Battery20';
import BatteryFullIcon from '@material-ui/icons/BatteryFull';
import AccordionTemps from "./AccordionTemps";
import TempCardTabs from './TempCardTabs'
import { Line } from 'react-chartjs-2';
import Battery50Icon from '@material-ui/icons/Battery50';
import TrendingUpIcon from '@material-ui/icons/TrendingUp';
import TrendingDownIcon from '@material-ui/icons/TrendingDown';
import TrendingFlatIcon from '@material-ui/icons/TrendingFlat';


const cardStyle = {
    maxHeight: "500px",
    overflow: "auto"
}
function BatteryInfo(prop) {
    if (prop.battery >= 4)
        return <Battery20Icon color={'error'}></Battery20Icon>
    else if (prop.battery === 0) return <BatteryFullIcon color={'primary'}></BatteryFullIcon>
    else return <Battery50Icon color={'action'}></Battery50Icon>
}

function VariationIndicator(prop) {
    let avg = 0
    let range = 10
    let firstMeasure = prop.data[0][prop.prop].toFixed(2);
    let margin = 0.3

    if(prop.data.length <= range){
        range = prop.data.length - 1
    }

    for (let i = 0; i < range; i++) {
        avg += prop.data[i + 1][prop.prop]
    }
    avg = (avg / range).toFixed(2)
    if(avg + margin >= firstMeasure && avg - margin <= firstMeasure) return <TrendingFlatIcon color="action"></TrendingFlatIcon>
    else if (avg > firstMeasure) return <TrendingDownIcon color="primary"></TrendingDownIcon>
    else return <TrendingUpIcon color="error"></TrendingUpIcon>
   
}

const hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23].reverse()

class TempCard extends React.Component {

    constructor(props) {
        super(props);
    }

    renderLastResults() {

        if (this.props.temps.length) {
            return (
                <div>
                    <Typography variant="h5" component="span" color="primary"> {this.props.temps[0].temp.toFixed(2)}ºC <VariationIndicator data={this.props.temps} prop="temp"></VariationIndicator> </Typography>
                    <Typography variant="h5" component="span" color="secondary">
                        {this.props.temps[0].humidity.toFixed(2)}%
                        <VariationIndicator data={this.props.temps} prop="humidity"></VariationIndicator>
                    </Typography>
                </div>
            )
        }
        else{
            return <Typography variant="h5" component="span" color="primary">La conexion cone este dispositivo no está disponible </Typography>

        }

    }

    getTempByHours(hour) {

        return this.props.temps.filter((temp) => {
            let date = new Date(temp.date)
            return date.getHours() === hour
        })


    }

    getSpread(){
        let ocurrences_number= 24;
        let spread =this.props.temps.length / ocurrences_number;
        if(spread < 1) return 1
        else return Math.trunc(spread)
    }

    dates() {

        let spread = this.getSpread();


        return this.props.temps.map((temp, index) => {
            if (index % spread === 0) {
                return new Date(temp.date).toLocaleTimeString()
            }

        }).filter(temp => {
            return typeof temp != "undefined"
        })
    }
    temps() {

        let spread = this.getSpread();


        return this.props.temps.map((temp, index) => {
            if (index % spread === 0)
                return temp.temp.toFixed(2)
        }).filter(temp => {
            return typeof temp != "undefined"
        })
    }
    humidity() {
        let spread = this.getSpread();

        return this.props.temps.map((temp, index) => {
            if (index % spread === 0)
                return temp.humidity.toFixed(2)
        }).filter(temp => {
            return typeof temp != "undefined"
        })
    }


    plot() {


        return {
            labels: this.dates().reverse(),
            datasets: [
                {
                    label: 'Temperatures',
                    data: this.temps().reverse(),
                    borderColor: "#003300",
                    backgroundColor: "#4c8c4a"
                },
                {
                    label: 'Humedad',
                    data: this.humidity().reverse(),
                    borderColor: "#000051",
                    backgroundColor: "#534bae"
                }
            ]
        }
    }




    render() {
        return (

            <Card >
                <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                        <BatteryInfo battery={this.props.sensorInfo.battery_low}></BatteryInfo>  Canal: {this.props.sensorInfo.channel}
                    </Typography>
                    <Typography color="textSecondary" gutterBottom>
                        Última Act {new Date(this.props.sensorInfo.last_updated).toLocaleString()}
                    </Typography>
                    <Typography variant="h5" component="h2">
                        {this.props.sensorInfo.name}
                        {this.renderLastResults()}

                    </Typography>

                    <TempCardTabs items={[
                        {
                            label: "Resumen 24h",
                            template: <div style={cardStyle}>
                                {hours.map((hour) => (
                                    <AccordionTemps key={hour} hour={hour} temps={this.getTempByHours(hour)} ></AccordionTemps>
                                ))}
                            </div>
                        },
                        {
                            label: "Gráficas",
                            template: <Line data={
                                this.plot()
                            }></Line>

                        }
                    ]}>

                    </TempCardTabs>



                </CardContent>

            </Card>





        )
    }

}
export default TempCard;

