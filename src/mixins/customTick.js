export default {
    customTick(){
        let tick;
        if (!Array.isArray(this.time) || !this.time.length){
          tick = 2;
        } else {
          tick = 0;
        }
        return tick},
}