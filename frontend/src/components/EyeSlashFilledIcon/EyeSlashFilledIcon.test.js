import { render } from "@testing-library/react";

import { EyeSlashFilledIcon } from "./EyeSlashFilledIcon.jsx";

describe("EyeSlashFilledIcon", () => {
  it("renders correctly", () => {
    const { container } = render(<EyeSlashFilledIcon />);

    expect(container).toMatchSnapshot();
  });
});
