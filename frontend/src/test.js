console.log('your first module');


const num = 20;
const arr = [1, 2, 3, 4];
const obj = {
    a: 0,
    b: function () { }
}
const foo = () => {
    const a = 0;
    const b = 20;
    return a + b;
}

export default num

export const bar = () => { }
export const zcar = 12345;