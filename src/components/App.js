import React from 'react'
import Container from '@material-ui/core/Container';
import axios from 'axios'
import TempCard from './TempCard'
import Grid from '@material-ui/core/Grid';





function ItemList(props) {

  if (props.data)
    return (
      <Grid container spacing={1}>
        {Object.keys(props.data).map((key) =>
          <Grid key={key} item xs={12} md={6}>
            <TempCard
              sensorInfo={props.data[key].sensorData}
              temps={props.data[key].temperatures}></TempCard>
          </Grid>
        )}
      </Grid>
    )
  else return <div></div>
}

class App extends React.Component {



  constructor(props) {
    super(props);

    this.state = {
      data: null,
    };
  }

  componentDidMount() {
    this.fetchData()
    setInterval(()=>{
      this.fetchData()
    }, 60000*5 )
  }

  fetchData(){
    axios.get('/fetch').then((response) => {
      this.setState({ data: response.data })
    })
  }


  render() {
    return (
      <Container maxWidth="lg">
        <ItemList data={this.state.data}></ItemList>
      </Container>
    );
  }

}



export default App