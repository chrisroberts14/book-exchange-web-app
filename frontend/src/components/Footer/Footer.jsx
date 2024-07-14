import {
    Navbar,
    NavbarBrand,
    NavbarContent,
    NavbarItem,
    Link,
    Divider
} from "@nextui-org/react";
import {GithubIcon} from "../icons.tsx";


export const Footer = () => {
    return (
        <Navbar
            maxWidth={"full"}
            className="flex h-32"
        >
            <NavbarBrand href="#">
            </NavbarBrand>
            <NavbarContent justify="center">
                <NavbarItem>
                    <div className="max-w-md">
                        <div className="flex h-5 items-center space-x-4 text-small">
                            <Link isExternal href="https://github.com/chrisroberts14/book-exchange-web-app"
                                  color="foreground">
                                <GithubIcon className="text-default-100" size="35"/>
                                <p style={{padding: "10px"}}>Github</p>
                            </Link>
                            <Divider orientation="vertical"/>
                            <div>Made by Christopher Roberts</div>
                        </div>
                    </div>
                </NavbarItem>
            </NavbarContent>
            <NavbarContent justify="end">
            </NavbarContent>
        </Navbar>
    );
};
