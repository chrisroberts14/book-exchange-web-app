import { render } from "@testing-library/react";

import { EyeFilledIcon } from "./EyeFilledIcon.jsx";

describe("EyeFilledIcon", () => {
  it("renders correctly", () => {
    const { container } = render(<EyeFilledIcon />);

    expect(container).toMatchSnapshot();
  });
});
