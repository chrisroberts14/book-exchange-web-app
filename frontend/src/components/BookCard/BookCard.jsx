import {Card, CardHeader, CardBody, Divider} from "@nextui-org/react";


export const BookCard = ({ book }) => {
    return (
        // Probably want to add a link to listings page here at some point
        <Card className="max-w-[400px] min-w-[400px]" data-testid="book-card">
            <CardHeader className="flex gap-10">
                <div className="flex flex-col">
                    <p className="text-md">{book.title}</p>
                    <p className="text-small text-default-500">By {book.author}</p>
                </div>
            </CardHeader>
            <Divider/>
            <CardBody>
                <p>{book.description}</p>
            </CardBody>
            <Divider/>
        </Card>
    );
}
