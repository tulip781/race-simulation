export default {
    customRange(){
        let range;
        if (!Array.isArray(this.time) || !this.time.length){
          range = [0, 10];
        } else {
          range = []
        }
        return range},
}