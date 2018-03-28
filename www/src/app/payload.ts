export class Payload {
  constructor(
    public thread: string,
    public action: string,
    public priority?: number,
    public status?: number,
    public data?: string
  ) {}
}
