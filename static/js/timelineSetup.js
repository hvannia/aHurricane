let container = document.getElementById('timeline');
let plotdiv=document.getElementById("eventPlot");
let mapdiv=document.getElementById("pathmap");
let infodiv= document.getElementById("eventInfo");
let gevents; //global copy of event response
let gclick; // global copy of click data 
let gpdata; // global copy of patg data
let ghdata; //global copy of single evenytheader data
let lastEvent=""; 
//let eventName="";
//let t=('1965-01-01', '1966-01-31') // default view area for timeline
//let gx;

  // Configuration for the Timeline  : http://visjs.org/docs/timeline/#Configuration_Options
  var options = { 
    zoomMax: 315360000000000
};

d3.json("/b_events").then(function(events){
    gevents = events;
    //console.log(events[0]);
    var timeline = new vis.Timeline(container, new vis.DataSet(events), options);
    timeline.setWindow('1964-01-01', '1965-01-31');
    timeline.on('click', function (clickObj) {
        gclick=clickObj;
        eventId=clickObj.item;
        console.log(clickObj);
       // if (eventId !== null  && lastEvent !=eventId){
        //    lastEvent=eventId
            drawGraphs(eventId);
       // }
    });  
});// end json to get timeline data 

function getColor(x){ 
    return x > 156 ? '#BD0026' :	//cat5
            x > 129 ? '#F03b20'	:	//cat4
            x > 110 ? '#FD8D3C'	:	//cat3
            x > 95	? '#FECC5C' :	//cat2
            x > 73	? '#FFFFB2'	:	//cat1
            x > 38	? '#B6F0B6'	:	//tstorm
                    '#DCE3DD'; 		//storm
}

function clearMap() {
    for(i in pathMap._layers) {
        if(pathMap._layers[i]._path != undefined) {
            try {
                pathMap.removeLayer(pathMap._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + pathMap._layers[i]);
            }
        }
    }
}


// get event specific data from /
function drawGraphs(eventID){  //replace with actual json query to use in line d3.json...
    /* main info about this event*/
    d3.json("/b_eventHeader/"+eventID).then(function(hdata){
        ghdata=hdata;
        eId=d3.select("#evenId");
        eId.text( eventID);
        eName=d3.select("#eventName");
        eName.text(Object.values(ghdata)[1][0]);
        eDates=d3.select("#eventDates");
        //eventDates
        sd = (new moment(hdata["sdate"][0].toString()).add(ghdata["stime"][0]/100,'hours'));
        ed = (new moment(hdata["edate"][0].toString()).add(ghdata["etime"][0]/100,'hours'));
       
        eDates.text(` ${ sd.format('MMMM Do YYYY, h a')} - \n  ${ ed.format('MMMM Do YYYY, h a')}`);
        eSpeed= d3.select("#eventSpeed");
        eSpeed.text(`Maximum winds of ${ghdata["ws"][0]} mph`);
      

    });
    /* start with map */



    d3.json("/b_events/"+eventID).then(function(pdata){ 
        clearMap();
        gpdata=pdata; //global copy
        lightmap.addTo(pathMap);
      
        var myStyle = {
            "color": getColor(d3.max(gpdata.features[0].properties.winds)),
            "weight": 2,
            "opacity": 0.5
        };
       L.geoJson(pdata, {
                style: myStyle
        }).addTo(pathMap)
        //pathMap.fitBounds(pathMap.getBounds());
        /* wind speed */
        let dates=gpdata.features[0].properties.dates;
        let winds=gpdata.features[0].properties.winds;
        //console.log(winds);
        let trace1 ={
            x:dates,
            y:winds,
            type:'scatter',
            fill: 'tozeroy',
        }
        let datas = [trace1];
        var layout = {
            title: 'Wind Speed throughout event '+eventID ,
            xaxis: {
              title: 'Time'
            },
            yaxis: {
              title: 'Max. Wind Speed (mph)'
            }
          };
        Plotly.newPlot('eventPlot', datas, layout);  

    });

}
