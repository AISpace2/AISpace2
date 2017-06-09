import * as d3 from 'd3';
import * as $ from 'jquery';
var recentreFlag:number;


function d3graph(el: HTMLElement, jsonProblem, view): void {
    console.time("D3 Graph Layout");
    var jsonProblem = JSON.parse(jsonProblem);
    //Ensure jquery is working
    $(document).ready(function () {

        //Detect if the passed in CSP has coordinates specified. If it does, use them later
        if (jsonProblem.hasOwnProperty("coordinates")) {
            var coords = jsonProblem.coordinates;
        }

        //build canvas for idempotency
        d3.select(el).select('svg').remove();
        var svg = d3.select(el).append("svg");
        if (coords) { //use the given coordinates to set width,height
            var width = 0;
            var height = 0;
            var node;
            for (node in coords[0]) { //find the maximum width, height
                if (coords[0][node][0] > width) {
                    width = coords[0][node][0];
                }
                if (coords[0][node][1] > height) {
                    height = coords[0][node][1];
                }
            }
            for (node in coords[1]) {
                if (coords[1][node][0] > width) {
                    width = coords[1][node][0];
                }
                if (coords[1][node][1] > height) {
                    height = coords[1][node][1];
                }
            }
            width = width + 25;
            height = height + 25;
        } else { //if no coordinates are supplied, use a standard size
            var width = el.clientWidth;
            var height = width / 2;
        }

        svg.attr("width", width)
            .attr("height", height);

        //create SVG containers for each set of elements of the graph
        svg.append("g").attr("id", "edges");
        svg.append("g").attr("id", "nodes");
        svg.append("g").attr("id", "conts");
        svg.append("g").attr("id", "labels");
        svg.append("g").attr("id", "domains");

        //create arrays to hold specific attributes of variables, constraints, and arcs
        //These will be used in the layout functions
        var forceVarList = [];
        var forceConList = [];
        var forceEdgeList = [];

        //Create graph elements
        //-------------Nodes (variables)-------------------

        var nodeData = jsonProblem.nodes;
        var variables = svg.select("#nodes").selectAll("ellipse")
            .data(nodeData)
            .enter().append("ellipse")
            .attr("id", function (d: any) {
                return d.name;
            })
            .classed("vertex", true)
            .attr("domain", function (d: any) {
                return d.domain;
            })
            .style("fill", "white")
            .style("stroke", "black")
            .attr("ry", 30)
            .attr("rx", function (d: any) { //set width of ellipse based on the size of the domain
                if (d.domain.length < 5) {
                    return 30;
                } else if (d.domain.length > 15) {
                    return 80;
                } else {
                    return 20 + d.domain.length * 4;
                }
            });

        if (coords) { //place ellipse at the coordinates specified
            d3.selectAll("ellipse")
                .attr("cx", function (d: any) {
                    return coords[0][d.name][0];
                })
                .attr("cy", function (d: any) {
                    return coords[0][d.name][1];
                });
        }
        variables.each(function (d: any, i) { //fill array for use in the layout
            if (!coords) {
                forceVarList.push({
                    fnid: d.name,
                    type: "varNode",
                    baseDomain: d.domain,
                    varIndex: i
                });
            } else {
                forceVarList.push({
                    fnid: d.name,
                    type: "varNode",
                    baseDomain: d.domain,
                    x: (+(this as any).getAttribute("cx")),
                    y: (+(this as any).getAttribute("cy")),
                    varIndex: i
                });
            }
        });
        variables.data(forceVarList);

        //----------Constraints (consts)----------

        var constData = jsonProblem.constraints;
        var consts = svg.select("#conts").selectAll("rect")
            .data(constData)
            .enter().append("rect")
            .attr("id", function (d: any) {
                var tId = d.string; //sanitize id-input string
                tId = tId.replace(/!/g, "n").replace(/=/g, "eq").replace(/[!@#$%^&*()-+={}\[\], <>?/\\'";:]/g, "_");
                return "con_" + tId;
            })
            .attr("label", function (d: any) {
                return d.string;
            })
            .classed("vertex", true)
            .attr("constraint", function (d: any) {
                return d.constraint;
            })
            .attr("nodes", function (d: any) {
                return d.nodes;
            })
            .style("fill", "white")
            .style("stroke", "black")
            .attr("height", 30);

        consts.each(function (d, i) {
            if ((this as any).getAttribute("label").length < 5) { //set width based on length of text
                (this as any).setAttribute("width", 50);
            } else {
                (this as any).setAttribute("width", ((this as any).getAttribute("label").length * 7) + 20)
            }
            if (coords) { //place rect at the coordinates specified
                (this as any).setAttribute("x", coords[1][i][0]);
                (this as any).setAttribute("y", coords[1][i][1]);
            }
        });
        consts.each(function (d, i) { //fill array for use in the layout
            if (!coords) {
                forceConList.push({
                    fnid: (this as any).id,
                    type: "constNode",
                    conIndex: i
                });
            } else {
                forceConList.push({
                    fnid: (this as any).id,
                    type: "constNode",
                    x: (+(this as any).getAttribute("x")),
                    y: (+(this as any).getAttribute("y")),
                    conIndex: i
                });
            }
        });

        //------------Edges (edges)------------
        consts.each(function (d: any) {
            for (var node in d.nodes) {
                d3.select("#edges").append("line") //sanitize constraint name
                    .attr("id", function () {
                        return "line-" + d.nodes[node] + "-" + d.string.replace(/!/g, "n").replace(/=/g, "eq").replace(/[!@#$%^&*()-+={}\[\], <>?/\\'";:]/g, "_");
                    })
                    .attr("src", (this as any).id)
                    .attr("dst", d.nodes[node])
                    .style("stroke-width", 1)
                    .style("stroke", "blue");
            }
        });
        var edges = d3.selectAll("#edges line");
        edges.each(function (d, i) {
            forceEdgeList.push({
                feid: (this as any).id, //fill array for use in the layout
                source: forceVarList.length + (+findNodeIndex((this as any).getAttribute("src"), forceConList)),
                target: (+findNodeIndex((this as any).getAttribute("dst"), forceVarList))
            });
        });
        edges.data(forceEdgeList);
        consts.data(forceConList);

        //Set mousehover behaviour
        $("line").hover(function () {
            d3.select(this).style("stroke-width", 5);
        }, function () {
            d3.select(this).style("stroke-width", 1);
        });
        $("line").click(function (e: any) {
            var data = e.target.__data__;
            view.constraintClicked(data.source.conIndex, data.target.fnid);
        });
        $("ellipse").hover(
            function () {
                d3.select(this).style("fill", "black");
                d3.select("#" + (this as any).id + "-label").style("fill", "white");
                d3.select("#" + (this as any).id + "-domain").style("fill", "white");
            },
            function () {
                d3.select(this).style("fill", "white");
                d3.select("#" + (this as any).id + "-label").style("fill", "black");
                d3.select("#" + (this as any).id + "-domain").style("fill", "black");
            });
        $("rect").hover(
            function () {
                d3.select(this).style("fill", "black");
                d3.select("#" + (this as any).id + "-label").style("fill", "white");
            },
            function () {
                d3.select(this).style("fill", "white");
                d3.select("#" + (this as any).id + "-label").style("fill", "black");

            });

        //------------Force Layout (setup)------------

        var renderIt = 1;
        //move each node (variables + constraints) to its new coordinates
        //move end points of each line (arc) to centre on its target
        function render() {
            renderIt += 1;
            variables
                .attr("cx", function (d: any) {
                    return d.x;
                })
                .attr("cy", function (d: any) {
                    return d.y;
                });
            consts //minor adjustments in node placing facilitate printing the label
                .attr("x", function (d: any) {
                    return d.x - ((this as any).getAttribute("width") / 2);
                })
                .attr("cx", function (d: any) {
                    return d.x;
                })
                .attr("y", function (d: any) {
                    return d.y - 15;
                })
                .attr("cy", function (d: any) {
                    return d.y + 15;
                });
            edges
                .attr("x1", function (d: any) {
                    return d.source.x
                })
                .attr("y1", function (d: any) {
                    return d.source.y
                })
                .attr("x2", function (d: any) {
                    return d.target.x
                })
                .attr("y2", function (d: any) {
                    return d.target.y
                });

            variables.each(function () {
                printLabel((this as any).id, (this as any).id);
                printDomain((this as any).id, (this as any).getAttribute("domain"));
            });
            consts.each(function () {
                printLabel((this as any).id, (this as any).getAttribute("label"));
            });
        }

        //Force function that keeps each node from going beyond the boundaries of the svg canvas
        function boundaryForce() {
            for (var i = 0, n = forceSim.nodes().length, node, top, side; i < n; ++i) {
                node = forceSim.nodes()[i];
                //side = half the width of a node-ish
                //top = half the height of a node
                if (node.type == "varNode") {
                    side = node.baseDomain.length * 8;
                    top = 35;
                } else {
                    side = node.fnid.length * 6;
                    top = 20;
                }
                if (node.x + node.vx > width - side) {
                    node.x = width - side;
                    node.vx = 0;
                }
                if (node.x + node.vx < side) {
                    node.x = side;
                    node.vx = 0;
                }
                if (node.y + node.vy > height - top) {
                    node.y = height - top;
                    node.vy = 0;
                }
                if (node.y + node.vy < top) {
                    node.y = top;
                    node.vy = 0;
                }
            }
        }

        //--------- Force Layout (forceSim)--------

        //Force Layout object that handles moving the nodes around (if no coordinates)
        //and drag/recentre/boundary effects (for both)
        var forceSim = d3.forceSimulation()
            .nodes(forceVarList.concat(forceConList))
            .velocityDecay(0.6)
            .force("gravity", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide(75))
            .force("boundaries", boundaryForce)
            .alpha(0.2)
            .on("tick", render)
            .on("end", function () {
                //--------- Draw labels and domains --    
                variables.each(function () {
                    printLabel((this as any).id, (this as any).id);
                    printDomain((this as any).id, (this as any).getAttribute("domain"));
                });
                consts.each(function () {
                    printLabel((this as any).id, (this as any).getAttribute("label"));
                });
            })
            .stop(); //layout proceeds automatically, so stop it to apply case-specific behaviour

        if (!coords) {
            recentreFlag = 1;
            forceSim //apply repellant and attractive forces between nodes/edges
                .force("spring", d3.forceLink(forceEdgeList).distance(35).strength(0.6))
                .force("charge", d3.forceManyBody().strength(-3500))
                .restart();
        } else {
            recentreFlag = 0;
            forceSim //apply minor repositioning
                .force("spring", d3.forceLink(forceEdgeList).distance(35).strength(0.0))
                .alpha(0.2)
                .alphaMin(0.1)
                .restart();
        }

        //-------- Drag (dragger)-------
        var dragger = d3.drag()
            .on("start", function () {
                d3.event.subject.active = true;
                forceSim.stop()
            })
            .on("drag", function () {
                d3.event.subject.x = d3.event.x;
                d3.event.subject.y = d3.event.y;
                render();
                if (d3.event.subject.type == "varNode") {
                    printDomain(d3.event.subject.fnid, d3.select("#" + d3.event.subject.fnid).attr("domain"));
                    printLabel(d3.event.subject.fnid, d3.event.subject.fnid);
                } else {
                    printLabel(d3.event.subject.fnid, d3.select("#" + d3.event.subject.fnid).attr("label"));
                }

            })
            .on("end", function () {
                d3.event.subject.active = false;
                if (recentreFlag == 1) {
                    forceSim.restart();
                }
            });
        var vertices = d3.selectAll(".vertex");
        vertices.call(dragger);

        //----------- Menu Bar ---------------

        /*var recentreFlag; //If set, dragging will reactivate the layout, effectively recentring the graph
        var menuDiv = d3.select("#menu");
        //create button for toggling recentring
        var recentreButton = menuDiv.append("button")
            .text("Graph Recentreing")
            .attr("id", "buttonCentre")
            .style("background-color", function () {
                if (recentreFlag == 1) {
                    return "#ccc";
                } else {
                    return "rgb(221, 221, 221)";
                }
            })
            .classed("toggleButton", true)
            .on('click', function () {
                recentreFlag = (recentreFlag + 1) % 2;
                if (recentreFlag) {
                    d3.select(this)
                        .style("background-color", "#ccc");
                } else {
                    d3.select(this)
                        .style("background-color", "rgb(221, 221, 221)");
                }
            });*/

        /*var tickButton = menuDiv.append("button")
            .text("tick")
            .attr("id", "buttonTick")
            .on('click', function(){
                console.log("ForceSim Lists", forceVarList, forceConList, forceEdgeList);
            });*/


        //----------- d3-using Utility functions -------
        // If I can figure out a way to include d3 in other JS src files
        // it will make this section useless. Using it for now though.

        function printDomain(nId, domainArr) {
            var node = d3.select("[id='" + nId + "']");
            var nodeText = d3.select('[id="' + nId + '-domain"]');
            if (nodeText.empty()) {
                d3.select("#domains").append("text")
                    .attr("x", node.attr("cx"))
                    .attr("y", (+node.attr("cy")) + 10)
                    .text("{" + domainArr + "}")
                    .attr("text-anchor", "middle")
                    .attr("id", nId + "-domain")
                    .style("pointer-events", "none");
            } else {
                nodeText
                    .attr("x", node.attr("cx"))
                    .attr("y", (+node.attr("cy")) + 10)
                    .text("{" + domainArr + "}")
                    .style("pointer-events", "none");
            }
            node.attr("rx", function () {
                if (domainArr.length < 5) {
                    return 30;
                } else {
                    return domainArr.length * 7
                }
            });
        }

        function printLabel(nId, labelStr) {
            var node = d3.select('[id="' + nId + '"]');
            var nodeText = d3.select('[id="' + nId + '-label"]');
            if (nodeText.empty()) {
                d3.select("#labels").append("text")
                    .attr("x", node.attr("cx"))
                    .attr("y", (+node.attr("cy")) - 10)
                    .text(labelStr)
                    .attr("text-anchor", "middle")
                    .attr("id", nId + "-label")
                    .style("pointer-events", "none");
            } else {
                nodeText
                    .attr("x", node.attr("cx"))
                    .attr("y", (+node.attr("cy")) - 10)
                    .text(labelStr);
            }
        }

        function findNodeIndex(str, nodes) {
            for (var index in nodes) {
                if (nodes[index].fnid == str)
                    return index;
            }
        }
        console.timeEnd("D3 Graph Layout")
    });
}

function reduceDomain(nodeId, dEl) {
    //remove the specified element from the specified node
    var dElement = "" + dEl;
    var tNode = d3.select("#" + nodeId);
    tNode.each(function (d: any) {
        var domain = (this as any).getAttribute("domain").split(',');
        var index = domain.indexOf(dElement);
        if (index != -1) { //remove element and replace domain
            domain.splice(index, 1);
            (this as any).setAttribute("domain", domain);
            printDomain(tNode.attr("id"), (this as any).getAttribute("domain"));
        } else {
            console.log("element not present in domain", dElement, (this as any).getAttribute("domain"));
        }
    });

    //Same functions as in setupTemplate
    function printDomain(nId, domainArr) {
        var node = d3.select("[id='" + nId + "']");
        var nodeText = d3.select('[id="' + nId + '-domain"]');
        if (nodeText.empty()) {
            d3.select("#domains").append("text")
                .attr("x", node.attr("cx"))
                .attr("y", (+node.attr("cy")) + 10)
                .text("{" + domainArr + "}")
                .attr("text-anchor", "middle")
                .attr("id", nId + "-domain");
        } else {
            nodeText
                .attr("x", node.attr("cx"))
                .attr("y", (+node.attr("cy")) + 10)
                .text("{" + domainArr + "}");
        }
        node.attr("rx", function () {
            if (domainArr.length < 5) {
                return 30;
            } else {
                return domainArr.length * 7
            }
        });
    }

    function printLabel(nId, labelStr) {
        var node = d3.select('[id="' + nId + '"]');
        var nodeText = d3.select('[id="' + nId + '-label"]');
        if (nodeText.empty()) {
            d3.select("#labels").append("text")
                .attr("x", +node.attr("cx"))
                .attr("y", +node.attr("cy") - 10)
                .text(labelStr)
                .attr("text-anchor", "middle")
                .attr("id", nId + "-label");
        } else {
            nodeText
                .attr("x", +node.attr("cx"))
                .attr("y", +node.attr("cy") - 10)
                .text(labelStr);
        }
    }
}

function highlightArc(variable, constraint, lineWeight, lineColour) {

    //Sanitize constraint name, and build arc name
    var fCon = constraint.replace(/!/g, "n").replace(/=/g, "eq").replace(/[!@#$%^&*()-+={}\[\], <>?/\\'";:]/g, "_");
    var arc = "line-" + variable + "-" + fCon;
    //console.log("Selected arc:",arc, d3.select("#"+arc));

    //Rather than select 1 arc, select all arcs and apply a style to them
    if (variable == "all" && constraint == "all") {
        d3.selectAll("line")
            .style("stroke", lineColour);
        if (lineWeight == "bold") {
            d3.selectAll("line")
                .style("stroke-width", 5);
        } else if (lineWeight == "!bold") {
            d3.selectAll("line")
                .style("stroke-width", 1);
        }
    } else {
        if (lineWeight == "bold") {
            d3.select("#" + arc).style("stroke-width", 5);
        } else if (lineWeight == "!bold") {
            d3.select("#" + arc).style("stroke-width", 1);
        }
        if (lineColour != "na") {
            d3.select("#" + arc).style("stroke", lineColour);
        }
    }
}
function restoreDomains() {
    //Reset a specific node
    function resetNodeDomain(nodeId) {
        var baseDomain;
        var node = d3.select('[id="' + nodeId + '"]')
            .attr("domain", function (d: any) {
                return d.baseDomain;
            });
        d3.select('[id="' + nodeId + '-domain"]')
            .text("{" + node.attr("domain") + "}")
            .attr("x", node.attr("cx"))
            .attr("y", (+node.attr("cy")) + 10);
    }

    //Select and reset all nodes
    var nodes = d3.selectAll("ellipse");
    nodes.each(function () {
        resetNodeDomain((this as any).id);
    });
}

export default {
    d3graph,
    highlightArc,
    reduceDomain
};