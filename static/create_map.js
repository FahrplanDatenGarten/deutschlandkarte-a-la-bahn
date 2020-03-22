var svg1 = d3.select("#net"), height = 800, width = 700;
var projection = d3.geoMercator()
    .scale(3000)
    .center([10, 51])
    .translate([width / 2, height / 2]);

var path = d3.geoPath()
    .projection(projection);


var promises = [
    d3.json(d3_geojson_url),
    d3.json(d3_api_url)
];
Promise.all(promises).then(ready);

function ready(param) {

    svg1.append("g")
        .selectAll("path")
        .data(param[0]["features"])
        .enter()
        .append("path")
        .attr("d", d3.geoPath()
            .projection(projection))
        .attr("fill", "#C0E1D7");

    var lineGenerator = d3.line();
    var pathGroup = svg1.append("g");
    var paths = pathGroup.selectAll("path")
        .data(param[1]['connections'])
        .enter()
        .append("path")
        .attr("stroke", "#000000")
        .attr("fill", "#000000")
        .attr("d", function (d, i) {
            return lineGenerator(d.link.map(projection))
        })
        .attr("stroke-width", function (d) {
            // console.log(this.getTotalLength())
            return (d.duration / this.getTotalLength()) / 8
        })
        .attr("opacity", 0.2)
        .attr("display", "none");

    svg1.append("g")
        .selectAll("circle")
        .data(param[1]['stations'])
        .enter()
        .append("circle")
        .attr("r", 5)
        .attr("fill", "#EC0016")
        .attr("transform", function (d, i) {
            return "translate(" + projection(d.location) + ")"
        })
        .on("click", function draw_lines(d, i) {
            paths.filter(path_data => {
                return JSON.stringify(path_data.link[0]) == JSON.stringify(d.location);
            })
                .attr("display", "block");
            paths.filter(path_data => {
                return JSON.stringify(path_data.link[0]) != JSON.stringify(d.location);
            })
                .attr("display", "none");
        })
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);
            
        function handleMouseOver(d, i) {  // Add interactivity
            // show station names
            svg1.append("text").text(d.name)
                .attr("transform", "translate(" + projection(d.location)+")")
        };
        

        function handleMouseOut(d, i) {
            // removing station names
            svg1.selectAll("text").remove()
        };

}
