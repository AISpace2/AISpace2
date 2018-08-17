export interface IObservation {
  /** The name of the observed node */
  name: string;
  /** The observation value made */
  value: string|boolean;
}

export class ObservationManager {
  private observations: IObservation[];

  public add(name: string, selectedDomain: any) {
    this.remove(name);

    if (typeof(selectedDomain) !== "boolean") {
      selectedDomain = selectedDomain.toString();
    }
    this.observations.push({"name": name, "value": selectedDomain});
  }

  public reset() {
    this.observations = [];
  }

  public remove(name: string) {
    this.observations = this.observations.filter((e:IObservation) => e.name !== name);
  }

  public dump(): IObservation[] {
    return this.observations;
  }

}
