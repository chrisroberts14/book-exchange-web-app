import { render } from "@testing-library/react";

import { NavbarComponent } from "./Navbar.jsx";

describe("NavbarComponent", () => {
  it("renders correctly logged in", () => {
    const { container } = render(<NavbarComponent signedIn={true} loggedIn={{name: ""}}/>);

    expect(container).toMatchSnapshot();
  });

  it("renders correctly logged out", () => {
    const { container } = render(<NavbarComponent signedIn={false} />);

    expect(container).toMatchSnapshot();
  });
});
