// Load the CSV file and create the chart
d3.csv("../data/airline_accidents.csv").then(data => {
    // Calculate the total incidents for each Make
    const incidentCounts = d3.rollup(
        data,
        v => v.length,
        d => d.Make.charAt(1).toUpperCase() + d.Make.slice(2).toLowerCase()
    );

    // Convert the Map to an array of objects and sort by incident count in descending order
    const incidentData = Array.from(incidentCounts, ([make, incidents]) => ({ make, incidents }))
        .sort((a, b) => b.incidents - a.incidents)  // Sort by incident count
        .slice(0, 10);  // Show only the top 10 makes

    // Set chart dimensions and margins
    const margin = { top: 30, right: 30, bottom: 100, left: 80 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG container
    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Set up the x-scale with only the top 10 makes
    const x = d3.scaleBand()
        .domain(incidentData.map(d => d.make))
        .range([0, width])
        .padding(0.1);

    // Set up the y-scale
    const y = d3.scaleLinear()
        .domain([0, d3.max(incidentData, d => d.incidents)])
        .nice()
        .range([height, 0]);

    // Create bars
    svg.selectAll(".bar")
        .data(incidentData)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.make))
        .attr("y", d => y(d.incidents))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.incidents))
        .attr("fill", "steelblue");

    // Add x-axis
    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");

    // Add y-axis
    svg.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("class", "axis-label")
        .attr("x", -20)
        .attr("y", -10)
        .attr("fill", "black")
        .style("text-anchor", "middle")
        .text("Incident Count");

    // Add chart title
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -10)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text("Top 10 Makes by Incident Count");
});
