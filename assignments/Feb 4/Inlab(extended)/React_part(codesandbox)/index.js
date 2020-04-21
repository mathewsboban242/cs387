import React, { useState } from "react";
import ReactDOM from "react-dom";

function Counter(props) {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1 )}> Counter: {props.name} {count} </button>;
}



const rootElement = document.getElementById("root");
ReactDOM.render(<div><Counter name="Raju"/></div>
, rootElement);

// ReactDOM.render(<div><Cell className="cell" name="H" at_number="1" gmu="g"/>
// { <Cell className="cell" name="H" at_number="1" gmu="m"/></div> }
// , rootElement);


function Container(props) {
  if(props.lookAndFeel=="label"){
  return (
    <div>
      Counter: {props.name}
    </div>
  );
  }
  else if(props.lookAndFeel=="button"){
  return <button> Counter: {props.name} </button>;
  }
}

function Cell(props){
  if(props.gmu=="g"){
    return (
      <div style={{color:"blue"}}>
        {props.at_number}   <br/>
        {props.name}
      </div>
    );
  }
  else if (props.gmu=="m"){
    return (
      <div style={{color:"red"}}>
        {props.at_number}   <br/>
        {props.name}     
      </div>
    );
  }
  else if (props.gmu=="u"){
    return (
      <div style={{color:"gray"}}>
        {props.at_number}   <br/>
        {props.name}
      </div>
    );
  }

}

