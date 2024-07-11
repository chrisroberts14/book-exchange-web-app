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
import { useState } from "react";

import { LoginSignUpForm } from "../LoginSignUpForm/LoginSignUpForm.jsx";

export const NavbarComponent = (input) => {
  const [state, setState] = useState("Listings");

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
        {input.signedIn ? (
          <AvatarDropdown user={input.loggedIn} />
        ) : (
          <LoginSignUp />
        )}
      </NavbarContent>
    </Navbar>
  );
};

export const LoginSignUp = () => {
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
          <LoginSignUpForm />
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};

export const AvatarDropdown = (user) => {
  return (
    <Dropdown placement="bottom-end">
      <DropdownTrigger>
        <Avatar
          isBordered
          as="button"
          className="transition-transform"
          color="secondary"
          name={user.user.name}
          size="sm"
        />
      </DropdownTrigger>
      <DropdownMenu aria-label="Profile Actions" variant="flat">
        <DropdownItem key="profile" className="h-14 gap-2">
          <p className="font-semibold">Signed in as</p>
          <p className="font-semibold">
            {user.user.name}
          </p>
        </DropdownItem>
        <DropdownItem key="user_settings">User Settings</DropdownItem>
        <DropdownItem key="user_books">Your Books</DropdownItem>
        <DropdownItem key="user_listings">Your Listings</DropdownItem>
        <DropdownItem key="logout" color="danger">
          Log Out
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};
