var margin = {
  top: 10,
  right: 10,
  bottom: 10,
  left: 10
};

var width = 960 - margin.left - margin.right;

var height = 500 - margin.top - margin.bottom;

var projection = d3.geoNaturalEarth1()
  .center([0, 15])
  .rotate([-9, 0])
  .scale([1300 / (2 * Math.PI)])
  .translate([450, 300]);

var path = d3.geoPath()
  .projection(projection);

var svg = d3.select("svg")
  .append("g")
  .attr("width", width)
  .attr("height", height);

var tooltip = d3.select("div.tooltip");

d3.queue()
  .defer(d3.json, "world.json")
  .defer(d3.csv, "names.csv")
  .await(ready);

function ready(error, world, names) {
  if (error) throw error;
  var countries1 = topojson.feature(world, world.objects.countries).features;
  countries = countries1.filter(function (d) {
    return names.some(function (n) {
      if (d.id == n.id) return d.name = n.name;
    })
  });

  svg.selectAll("path")
    .data(countries)
    .enter()
    .append("path")
    .attr("stroke-width", 1)
    .attr("fill", "white")
    .attr("d", path)
    .on("mouseover", function (d, i) {
      d3.select(this).attr("fill", "grey").attr("stroke-width", 2);
      return tooltip.style("hidden", false).html(d.name);
    })
    .on("mousemove", function (d) {
      tooltip.classed("hidden", false)
        .style("top", (d3.event.pageY) + "px")
        .style("left", (d3.event.pageX + 10) + "px")
        .html("Nome: " + d.name);
    })
    .on("mouseout", function (d, i) {
      d3.select(this).attr("fill", "white").attr("stroke-width", 1);
      tooltip.classed("hidden", true);
    });

  var zoom_handler = d3.zoom()
    .on("zoom", zoom_actions);

  function zoom_actions() {
    d3.selectAll("path").attr("transform", d3.event.transform);
  }

  zoom_handler(svg);
};