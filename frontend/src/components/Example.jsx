import React from 'react';
import { useState, useEffect } from 'react';
import Button from "@mui/material/Button";
import { Paper } from '@mui/material';

const Example = (props) => {
    const message = props.message || "Hallo";
    const divstyle = {
        "backgroundColor":"lightblue",
        "width":"fit-content",
        "padding":"20px",
        "border":"5px",
        "borderColor": "black",
        "margin":"50px"
        };

    const [counter, setCounter] = useState(0);

    function hello(){
        setCounter(counter+1);
    }

    return (        
        <>
        <Paper elevation={20} style={{"margin":"50px"}}>

        <p>{message} Welt</p>
        <div style={{"display":"flex", "justifyContent":"center", "gap":"20px"}}>

        <div style={divstyle}>Das ist ein div</div>
        <div style={divstyle}>Das ist ein div</div>
        </div>
        <div>{counter}</div>
        <Button onClick={hello} variant="contained">Knopf</Button>
        </Paper>
        </>
    );
}

export default Example;
