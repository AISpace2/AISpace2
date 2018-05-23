<script lang="ts">
  import Vue, { ComponentOptions } from "vue";
  import Component from "vue-class-component";
  import { Prop } from "vue-property-decorator";
  import BaseEdge from "./BaseEdge.vue";

  /**
   * An edge with an arrow pointing to the target, with support for text.
   */
  @Component
  export default class DirectedRectEdge extends BaseEdge {
    @Prop() graph_node_width: number;
    @Prop() graph_node_height: number;
    @Prop({default: 15}) textSize: number;
    // Minimum text width so that the node doesn't become too small when the text is short
    minTextWidth = 50;

    /** The x-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
    get adjustedX1() {
      return this.pathLength === 0 ? 0 : this.x1;
    }

    /** The y-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
    get adjustedY1() {
      if (this.pathLength === 0) return 0;
      return this.y1;
    }

    /** The x-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
    get adjustedX2() {
      let point = this.intersectPoint();
      return point ? point.x : this.x2;
    }

    /** The y-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
    get adjustedY2() {
      let point = this.intersectPoint();
      return point ? point.y : this.y2;
    }

    /* The idea is to find the (x, y) by making four linear test lines (y = mx + b) along the boundary of the target box.
        * Then find the intersection point between the directed rect edge and the test lines. Since expressing the edge in
        * y = mx + b form will stretch it infinitely, there would be two points touching. We find the one test intersect point,
        *  (ix, iy) where x1 <= ix <= x2 or if the two boxes are on the same x axis, we test for y where
        *   y1 <= iy <= y2. The point that fits the given condition will be where the edges points to. */


    /* Slope of the edge */
    slope() : number {
      if(this.deltaX === 0){
        // since delta X cannot be 0 as the denominator for calculating slope, we set it to as close to 0 as possible for
        // slope calculation
        return this.deltaY / 0.00005;
      }
      return this.deltaY/this.deltaX;
    }

    /* The edge is y = mx + b. This intercept is b */
    intercept() : number {
      return this.y1 - this.slope()*this.x1;
    }

    /* Intercept of the edge and the given test vertical line x = dx */
    intersectX(dx: number){
        return{ x: dx, y: this.slope()*dx+this.intercept()};
    }

    /* Intercept of the edge and the given test horizontal line y = dy */
    intersectY(dy: number){
      return {x: (dy-this.intercept())/this.slope(), y: dy};
    }

    intersectPoint() : {x: number, y:number} {
      const xLeft = this.x2 - this.graph_node_width/2;
      const xRight = this.x2 + this.graph_node_width/2;
      const yUp = this.y2 + this.graph_node_height/2;
      const yDown = this.y2 - this.graph_node_height/2;

      // setting the valid range for x and y (the range between the two graph nodes for the edge)
      const xBound = this.x1 < this.x2
        ? {lower: this.x1, upper: this.x2} : {lower: this.x2, upper: this.x1};
      const yBound = this.y1 < this.y2
        ? {lower: this.y1, upper: this.y2} : {lower: this.y2, upper: this.y1};

      return [
        this.intersectX(xLeft),
        this.intersectX(xRight),
        this.intersectY(yUp),
        this.intersectY(yDown)
      ].reduce((acc, point)=>{
        if(point.x >= xLeft && point.x <= xRight && point.y <= yUp && point.y >= yDown){
          if(point.x >= xBound.lower && point.x <= xBound.upper){
            acc = point;
          } else if(point.y >= yBound.lower && point.y <= yBound.upper) {
            acc = point;
          }
        }
        return acc;
      }, null);
    }
  }

</script>
