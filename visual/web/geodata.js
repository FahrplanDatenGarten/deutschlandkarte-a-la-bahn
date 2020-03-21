function createMap() {
    var svg1 = d3.select("#net"), height = 800, width = 700;
    var projection = d3.geoMercator()
        .scale(3000)
        .center([10, 51])
        .translate([width / 2, height / 2]);

    var path = d3.geoPath()
        .projection(projection);


    var promises = [
        d3.json("4_niedrig.geojson"),
        d3.json("test.json")
    ];
    Promise.all(promises).then(ready);

    function ready(parm) {

        svg1.append("g")
            .selectAll("path")
            .data(parm[0]["features"])
            .enter()
            .append("path")
            .attr("d", d3.geoPath()
                .projection(projection))
            .attr("fill", "red");

        for(var k in parm[1]){
            console.log(parm[1][k])
            
        }

    }

}

createMap();