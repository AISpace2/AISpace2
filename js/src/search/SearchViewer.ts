import * as widgets from "jupyter-js-widgets";
import {IEvent} from "../Events";
import {Graph} from "../Graph";
import SearchViewerModel from "./SearchViewerModel";

export default class SearchViewer extends widgets.DOMWidgetView {
    public model: SearchViewerModel;

    public initialize(opts: any) {
        super.initialize(opts);

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
        });
    }

    public render() {
        this.$el.html("<h1>hi</h1>");
    }
}
