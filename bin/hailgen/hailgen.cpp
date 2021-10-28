#include <SFML/Graphics.hpp>


int main()
{
    sf::RenderTexture renderTexture;
    renderTexture.create(490, 280);


    sf::Texture t_picture;
    t_picture.loadFromFile("assets/input.png");
    sf::Sprite s_picture;
    s_picture.setTexture(t_picture);
    s_picture.setOrigin(sf::Vector2f(t_picture.getSize().x / 2.f, t_picture.getSize().y / 2.f));
    s_picture.setPosition(sf::Vector2f(140.f, 120.f));

    sf::Texture t_frame;
    sf::Sprite s_frame;
    for (short frame_no = 1; frame_no <= 30; frame_no++) {
        t_frame.loadFromFile("assets/frames/frame" + std::to_string(frame_no) + ".png");
        s_frame.setTexture(t_frame);
        renderTexture.clear();
        renderTexture.draw(s_picture);
        renderTexture.draw(s_frame);
        renderTexture.display();
        renderTexture.getTexture().copyToImage().saveToFile("assets/out/frame" + std::to_string(frame_no) + ".png");
    }



    return 0;
}
