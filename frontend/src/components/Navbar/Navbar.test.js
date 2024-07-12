import {fireEvent, render, screen} from "@testing-library/react";

import {AvatarDropdown, NavbarComponent} from "./Navbar.jsx";

describe("NavbarComponent", () => {
  let setState;

  beforeEach(() => {
    setState = jest.fn();
  });

  it("renders correctly logged in", () => {
    const { container } = render(<NavbarComponent user={"test"} setState={setState}/>);
    expect(container).toMatchSnapshot();
  });

  it("renders correctly logged out", () => {
    const { container } = render(<NavbarComponent setState={setState}/>);
    expect(container).toMatchSnapshot();
  });
});

describe("Avatar Dropdown", () => {
  let setUser, user;

  beforeEach(() => {
    setUser = jest.fn();
  });

  it("renders correctly", () => {
    const { container } = render(<AvatarDropdown user={user} setUser={setUser} />);
    expect(container).toMatchSnapshot();
  });

  it('logs out correctly', () => {
    render(<AvatarDropdown user={user} setUser={setUser} />);
    fireEvent.click(screen.getByTestId("user-dropdown-open"));
    fireEvent.click(screen.getByTestId("logout-button"));
    expect(setUser).toHaveBeenCalled();
  });
});
