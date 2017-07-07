declare module "*.json" {
    const value: any;
    export default value;
}

declare module "*.html" {
    const value: any;
    export default value;
}

declare module "*.vue" {
    const value: any;
    export default value;
}

declare module "shortid" {
    export function generate(): string;
}