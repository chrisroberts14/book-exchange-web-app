import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  DropdownTrigger,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Avatar,
  Tabs,
  Tab,
} from "@nextui-org/react";

import { LoginSignUpForm } from "../LoginSignUpForm/LoginSignUpForm.jsx";

export const NavbarComponent = (input) => {
  return (
    <Navbar
      shouldHideOnScroll
      classNames={{
        item: [
          "flex",
          "relative",
          "h-full",
          "items-center",
          "data-[active=true]:after:content-['']",
          "data-[active=true]:after:absolute",
          "data-[active=true]:after:bottom-0",
          "data-[active=true]:after:left-0",
          "data-[active=true]:after:right-0",
          "data-[active=true]:after:h-[3px]",
          "data-[active=true]:after:rounded-[2px]",
          "data-[active=true]:after:bg-primary",
          "data-[active=true]:after:color-primary",
        ],
      }}
      maxWidth={"full"}
    >
      <NavbarBrand href="#">
        <p className="font-bold text-inherit">Book Exchange</p>
      </NavbarBrand>
      <NavbarContent justify="center">
        <NavbarItem>
          <Tabs
            aria-label="Tabs radius"
            className="gap-36"
            color="primary"
            size="lg"
          >
            <Tab key="listings" title="Listings" />
            <Tab key="books" title="Books" />
            <Tab key="users" title="Users" />
          </Tabs>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        {input.user ? (
          <AvatarDropdown user={input.loggedIn} setUser={input.setUser} />
        ) : (
          <LoginSignUp setUser={input.setUser} />
        )}
      </NavbarContent>
    </Navbar>
  );
};

export const LoginSignUp = (input) => {
  return (
    <Dropdown closeOnSelect={false} placement="bottom-end">
      <DropdownTrigger>
        <Avatar
          isBordered
          as="button"
          className="transition-transform"
          color="secondary"
          name="Account"
          size="sm"
        />
      </DropdownTrigger>
      <DropdownMenu aria-label="Profile Actions">
        <DropdownItem key="sign-in-log-in" isReadOnly>
          <LoginSignUpForm setUser={input.setUser}/>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};

export const AvatarDropdown = ({user, setUser}) => {
  return (
    <Dropdown placement="bottom-end">
      <DropdownTrigger data-testid="user-dropdown-open">
        <Avatar
          isBordered
          as="button"
          className="transition-transform"
          color="secondary"
          name={user}
          size="sm"
        />
      </DropdownTrigger>
      <DropdownMenu aria-label="Profile Actions" variant="flat">
        <DropdownItem key="profile" className="h-14 gap-2" textValue="Profile">
          <p className="font-semibold">Signed in as</p>
          <p className="font-semibold">
            {user}
          </p>
        </DropdownItem>
        <DropdownItem key="user_settings" textValue="User Settings">User Settings</DropdownItem>
        <DropdownItem key="user_books" textValue="Your Books">Your Books</DropdownItem>
        <DropdownItem key="user_listings" textValue="Your Listings">Your Listings</DropdownItem>
        <DropdownItem key="logout" color="danger" data-testid="logout-button" onPress={() => {window.localStorage.clear(); setUser(null);}} textValue="Log Out">Log Out</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};
