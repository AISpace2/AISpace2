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

    slope() : number {
      if(this.deltaX === 0){
        return this.deltaY / 0.00001;
      }
      return this.deltaY/this.deltaX;
    }

    intercept() : number {
      return this.y1 - this.slope()*this.x1;
    }

    intersectX(dx: number){
        return{ x: dx, y: this.slope()*dx+this.intercept()};
    }

    intersectY(dy: number){
      return {x: (dy-this.intercept())/this.slope(), y: dy};
    }

    intersectPoint() : {x: number, y:number} {
      let width = 105;
      let height = 45;
      let xLeft = this.x2-width/2;
      let xRight = this.x2+width/2;
      let yUp = this.y2+height/2;
      let yDown = this.y2-height/2;
      let i1 = this.intersectX(xLeft);
      let i2 = this.intersectX(xRight);
      let i3 = this.intersectY(yUp);
      let i4 = this.intersectY(yDown);

      let validPoints : [{x: number, y: number}] = [i1,i2,i3,i4].reduce((acc, point)=>{
        if(point.x >= xLeft && point.x <= xRight && point.y <= yUp && point.y >= yDown){
          acc.push(point);
        }
        return acc;
      }, []);
      let smallX = this.x1 < this.x2 ? this.x1 : this.x2;
      let largeX = this.x1 < this.x2 ? this.x2 : this.x1;
      let smallY = this.y1 < this.y2 ? this.y1 : this.y2;
      let largeY = this.y1 < this.y2 ? this.y2 : this.y1;
      validPoints = validPoints.reduce((acc, point)=>{
        if(point.x >= smallX && point.x <= largeX){
          acc.push(point);
        } else if(point.y >= smallY && point.y <= largeY) {
          acc.push(point);
        }
        return acc;
      }, []);
      return validPoints[0];
    }
  }

</script>
